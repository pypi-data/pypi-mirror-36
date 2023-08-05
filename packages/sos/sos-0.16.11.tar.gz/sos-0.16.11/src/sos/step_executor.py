#!/usr/bin/env python3
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

import contextlib
import copy
import fnmatch
import glob
import os
import re
import subprocess
import sys
import time
import traceback
from collections import Iterable, Mapping, Sequence, defaultdict
from io import StringIO
from itertools import combinations, tee
from typing import Any, Dict, List, Optional, Tuple, Union

import psutil
from billiard import Pool

from .eval import SoS_eval, SoS_exec, stmtHash, accessed_vars

from .parser import SoS_Step
from .pattern import extract_pattern
from .signatures import workflow_signatures
from .syntax import (SOS_DEPENDS_OPTIONS, SOS_INPUT_OPTIONS,
                     SOS_OUTPUT_OPTIONS, SOS_RUNTIME_OPTIONS, SOS_TAG)
from .targets import (BaseTarget, RemovedTarget, RuntimeInfo, UnavailableLock,
                      UnknownTarget, dynamic, file_target, path, paths, remote,
                      sos_targets, sos_step)
from .tasks import MasterTaskParams, TaskParams, TaskFile
from .utils import (SlotManager, StopInputGroup, TerminateExecution, ArgumentError, env,
                    expand_size, format_HHMMSS, get_traceback, short_repr)

__all__ = []


class PendingTasks(Exception):
    def __init__(self, tasks: List[Tuple[str, str]], *args, **kwargs) -> None:
        super(PendingTasks, self).__init__(*args, **kwargs)
        self.tasks = tasks


def analyze_section(section: SoS_Step, default_input: Optional[sos_targets] = None) -> Dict[str, Any]:
    '''Analyze a section for how it uses input and output, what variables
    it uses, and input, output, etc.'''
    from .workflow_executor import __null_func__
    from ._version import __version__

    # these are the information we need to build a DAG, by default
    # input and output and undetermined, and there are no variables.
    #
    # step input and output can be true "Undetermined", namely unspecified,
    # can be dynamic and has to be determined at run time, or undetermined
    # at this stage because something cannot be determined now.
    step_input: sos_targets = sos_targets()
    step_output: sos_targets = sos_targets()
    step_depends: sos_targets = sos_targets([])
    environ_vars = set()
    signature_vars = set()
    changed_vars = set()
    #
    # 1. execute global definition to get a basic environment
    #
    # FIXME: this could be made much more efficient
    if 'provides' in section.options:
        if '__default_output__' in env.sos_dict:
            step_output = env.sos_dict['__default_output__']
    else:
        # env.sos_dict = WorkflowDict()
        env.sos_dict.set('__null_func__', __null_func__)
        # initial values
        env.sos_dict.set('SOS_VERSION', __version__)
        SoS_exec('import os, sys, glob', None)
        SoS_exec('from sos.runtime import *', None)

    env.logger.trace(
        f'Analyzing {section.step_name()} with step_output {step_output}')

    #
    # Here we need to get "contant" values from the global section
    # Because parameters are considered variable, they has to be
    # removed. We achieve this by removing function sos_handle_parameter_
    # from the SoS_dict namespace
    #
    if section.global_def:
        try:
            SoS_exec('del sos_handle_parameter_\n' + section.global_def)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(e.stderr)
        except RuntimeError as e:
            if env.verbosity > 2:
                sys.stderr.write(get_traceback())
            raise RuntimeError(
                f'Failed to execute statements\n"{section.global_def}"\n{e}')
        finally:
            SoS_exec('from sos.runtime import sos_handle_parameter_', None)

    #
    # 2. look for input statement
    if 'shared' in section.options:
        svars = section.options['shared']
        if isinstance(svars, str):
            changed_vars.add(svars)
            svars = {svars: svars}
        elif isinstance(svars, Sequence):
            for item in svars:
                if isinstance(item, str):
                    changed_vars.add(item)
                elif isinstance(item, Mapping):
                    changed_vars |= set(item.keys())
                else:
                    raise ValueError(
                        f'Option shared should be a string, a mapping of expression, or list of string or mappings. {svars} provided')
        elif isinstance(svars, Mapping):
            changed_vars |= set(svars.keys())
        else:
            raise ValueError(
                f'Option shared should be a string, a mapping of expression, or list of string or mappings. {svars} provided')

    # look for input statement.
    input_statement_idx = [idx for idx, x in enumerate(
        section.statements) if x[0] == ':' and x[1] == 'input']
    if not input_statement_idx:
        input_statement_idx = None
    elif len(input_statement_idx) == 1:
        input_statement_idx = input_statement_idx[0]
    else:
        raise RuntimeError(
            f'More than one step input are specified in step {section.name if section.index is None else f"{section.name}_{section.index}"}')

    # if there is an input statement, analyze the statements before it, and then the input statement
    if input_statement_idx is not None:
        # execute before input stuff
        for statement in section.statements[:input_statement_idx]:
            if statement[0] == ':':
                if statement[1] == 'depends':
                    environ_vars |= accessed_vars(statement[2])
                    key, value = statement[1:3]
                    try:
                        args, kwargs = SoS_eval(f'__null_func__({value})')
                        if any(isinstance(x, (dynamic, remote)) for x in args):
                            step_depends = sos_targets()
                        else:
                            step_depends = _expand_file_list(True, *args)
                    except Exception as e:
                        env.logger.debug(
                            f"Args {value} cannot be determined: {e}")
                else:
                    raise RuntimeError(
                        f'Step input should be specified before {statement[1]}')
            else:
                environ_vars |= accessed_vars(statement[1])
        #
        # input statement
        stmt = section.statements[input_statement_idx][2]
        try:
            environ_vars |= accessed_vars(stmt)
            args, kwargs = SoS_eval(f'__null_func__({stmt})')

            if not args:
                if default_input is None:
                    step_input = sos_targets()
                else:
                    step_input = default_input
            elif not any(isinstance(x, (dynamic, remote)) for x in args):
                step_input = _expand_file_list(True, *args)
            env.sos_dict.set('input', step_input)

            if 'paired_with' in kwargs:
                pw = kwargs['paired_with']
                if pw is None or not pw:
                    pass
                elif isinstance(pw, str):
                    environ_vars.add(pw)
                elif isinstance(pw, Iterable):
                    environ_vars |= set(pw)
                elif isinstance(pw, Iterable):
                    # value supplied, no environ var
                    environ_vars |= set()
                else:
                    raise ValueError(
                        f'Unacceptable value for parameter paired_with: {pw}')
            if 'group_with' in kwargs:
                pw = kwargs['group_with']
                if pw is None or not pw:
                    pass
                elif isinstance(pw, str):
                    environ_vars.add(pw)
                elif isinstance(pw, Iterable):
                    environ_vars |= set(pw)
                elif isinstance(pw, Iterable):
                    # value supplied, no environ var
                    environ_vars |= set()
                else:
                    raise ValueError(
                        f'Unacceptable value for parameter group_with: {pw}')
            if 'for_each' in kwargs:
                fe = kwargs['for_each']
                if fe is None or not fe:
                    pass
                elif isinstance(fe, str):
                    environ_vars |= set([x.strip() for x in fe.split(',')])
                elif isinstance(fe, Sequence):
                    for fei in fe:
                        environ_vars |= set([x.strip()
                                             for x in fei.split(',')])
                else:
                    raise ValueError(
                        f'Unacceptable value for parameter fe: {fe}')
        except Exception as e:
            # if anything is not evalutable, keep Undetermined
            env.logger.debug(
                f'Input of step {section.name if section.index is None else f"{section.name}_{section.index}"} is set to Undertermined: {e}')
            # expression ...
            step_input = sos_targets(undetermined=stmt)
        input_statement_idx += 1
    else:
        # assuming everything starts from 0 is after input
        input_statement_idx = 0

    # other variables
    for statement in section.statements[input_statement_idx:]:
        # if input is undertermined, we can only process output:
        if statement[0] == '=':
            signature_vars |= accessed_vars('='.join(statement[1:3]))
        elif statement[0] == ':':
            key, value = statement[1:3]
            # if key == 'depends':
            environ_vars |= accessed_vars(value)
            # output, depends, and process can be processed multiple times
            try:
                args, kwargs = SoS_eval(f'__null_func__({value})')
                if not any(isinstance(x, (dynamic, remote)) for x in args):
                    if key == 'output':
                        step_output = _expand_file_list(True, *args)
                    elif key == 'depends':
                        step_depends = _expand_file_list(True, *args)
            except Exception as e:
                env.logger.debug(f"Args {value} cannot be determined: {e}")
        else:  # statement
            signature_vars |= accessed_vars(statement[1])
    # finally, tasks..
    if section.task:
        signature_vars |= accessed_vars(section.task)
    if 'provides' in section.options and '__default_output__' in env.sos_dict and step_output.valid():
        for out in env.sos_dict['__default_output__']:
            # 981
            if not isinstance(out, sos_step) and out not in step_output:
                raise ValueError(
                    f'Defined output fail to produce expected output: {step_output} generated, {env.sos_dict["__default_output__"]} expected.')

    return {
        'step_name': f'{section.name}_{section.index}' if isinstance(section.index, int) else section.name,
        'step_input': step_input,
        'step_output': step_output,
        'step_depends': step_depends,
        # variables starting with __ are internals...
        'environ_vars': {x for x in environ_vars if not x.startswith('__')},
        'signature_vars': {x for x in signature_vars if not x.startswith('__')},
        'changed_vars': changed_vars
    }


class TaskManager:
    # manage tasks created by the step
    def __init__(self, trunk_size, trunk_workers):
        super(TaskManager, self).__init__()
        self.trunk_size = trunk_size
        self.trunk_workers = trunk_workers
        self._submitted_tasks = []
        self._unsubmitted_tasks = []
        # derived from _unsubmitted_tasks
        self._all_ids = []
        self._all_output = []
        #
        self._terminate = False
        #
        self._tags = {}

    def append(self, task_def):
        self._unsubmitted_tasks.append(task_def)
        if isinstance(task_def[2], Sequence):
            self._all_output.extend(task_def[2])
        self._all_ids.append(task_def[0])
        self._tags[task_def[0]] = task_def[1].tags

    def tags(self, task_id):
        return self._tags.get(task_id, [])

    def has_task(self, task_id):
        return task_id in self._all_ids

    def has_output(self, output):
        if not isinstance(output, Sequence) or not self._unsubmitted_tasks:
            return False
        return any(x in self._all_output for x in output)

    def get_job(self, all_tasks=False):
        # save tasks
        if not self._unsubmitted_tasks:
            return None
        # single tasks
        if self.trunk_size == 1 or all_tasks:
            to_be_submitted = self._unsubmitted_tasks
            self._unsubmitted_tasks = []
        else:
            # save complete blocks
            num_tasks = len(
                self._unsubmitted_tasks) // self.trunk_size * self.trunk_size
            to_be_submitted = self._unsubmitted_tasks[: num_tasks]
            self._unsubmitted_tasks = self._unsubmitted_tasks[num_tasks:]

        # save tasks
        ids = []
        if self.trunk_size == 1 or (all_tasks and len(self._unsubmitted_tasks) == 1):
            for task_id, taskdef, _ in to_be_submitted:
                # if the task file, perhaps it is already running, we do not change
                # the task file. Otherwise we are changing the status of the task
                TaskFile(task_id).save(taskdef)
                ids.append(task_id)
        else:
            master = None
            for task_id, taskdef, _ in to_be_submitted:
                if master is not None and master.num_tasks() == self.trunk_size:
                    ids.append(master.ID)
                    TaskFile(master.ID).save(master)
                    master = None
                if master is None:
                    master = MasterTaskParams(self.trunk_workers)
                master.push(task_id, taskdef)
            # the last piece
            if master is not None:
                TaskFile(master.ID).save(master)
                ids.append(master.ID)

        if not ids:
            return None

        self._submitted_tasks.extend(ids)
        return ids

    def clear_submitted(self):
        self._submitted_tasks = []


# overwrite concurrent_execute defined in Base_Step_Executor because sos notebook
# can only handle stdout/stderr from the master process
#
@contextlib.contextmanager
def stdoutIO():
    oldout = sys.stdout
    olderr = sys.stderr
    stdout = StringIO()
    stderr = StringIO()
    sys.stdout = stdout
    sys.stderr = stderr
    yield stdout, stderr
    sys.stdout = oldout
    sys.stderr = olderr


def validate_step_sig(sig):
    if env.config['sig_mode'] == 'default':
        # if users use sos_run, the "scope" of the step goes beyong names in this step
        # so we cannot save signatures for it.
        if 'sos_run' in env.sos_dict['__signature_vars__']:
            return {}
        else:
            matched = sig.validate()
            if isinstance(matched, dict):
                env.logger.info(
                    f'``{env.sos_dict["step_name"]}`` (index={env.sos_dict["_index"]}) is ``ignored`` due to saved signature')
                return matched
            else:
                env.logger.debug(
                    f'Signature mismatch: {matched}')
                return {}
    elif env.config['sig_mode'] == 'assert':
        matched = sig.validate()
        if isinstance(matched, str):
            raise RuntimeError(
                f'Signature mismatch: {matched}')
        else:
            env.logger.info(
                f'Step ``{env.sos_dict["step_name"]}`` (index={env.sos_dict["_index"]}) is ``ignored`` with matching signature')
            return matched
    elif env.config['sig_mode'] == 'build':
        # build signature require existence of files
        if 'sos_run' in env.sos_dict['__signature_vars__']:
            return {}
        elif sig.write(rebuild=True):
            env.logger.info(
                f'Step ``{env.sos_dict["step_name"]}`` (index={env.sos_dict["_index"]}) is ``ignored`` with signature constructed')
            return {'input': sig.content['input'],
                'output': sig.content['output'],
                'depends': sig.content['depends'],
                'vars': sig.content['end_context']
                }
    elif env.config['sig_mode'] == 'force':
        return {}
    else:
        raise RuntimeError(
            f'Unrecognized signature mode {env.config["sig_mode"]}')


def concurrent_execute(stmt, proc_vars={}, step_md5=None, step_tokens=[],
    shared_vars=[], capture_output=False):
    '''Execute statements in the passed dictionary'''
    # prepare a working environment with sos symbols and functions
    from .workflow_executor import __null_func__
    from ._version import __version__
    env.sos_dict.set('__null_func__', __null_func__)
    # initial values
    env.sos_dict.set('SOS_VERSION', __version__)
    SoS_exec('import os, sys, glob', None)
    SoS_exec('from sos.runtime import *', None)
    # update it with variables passed from master process
    env.sos_dict.quick_update(proc_vars)
    sig = None if env.config['sig_mode'] == 'ignore' or env.sos_dict['_output'].unspecified() else RuntimeInfo(
        step_md5, step_tokens,
        env.sos_dict['_input'],
        env.sos_dict['_output'],
        env.sos_dict['_depends'],
        env.sos_dict['__signature_vars__'],
        shared_vars=shared_vars)
    outmsg = ''
    errmsg = ''
    try:
        if sig:
            matched = validate_step_sig(sig)
            if matched:
                # avoid sig being released in the final statement
                sig = None
                return {'ret_code': 0, 'sig_skipped': 1, 'output': matched['output'], 'shared': matched['vars']}
            sig.lock()
        verify_input()

        if capture_output:
            with stdoutIO() as (out, err):
                SoS_exec(stmt, return_result=False)
                outmsg = out.getvalue()
                errmsg = err.getvalue()
        else:
            SoS_exec(stmt, return_result=False)
        if env.sos_dict['step_output'].undetermined():
            # the pool worker does not have __null_func__ defined
            env.sos_dict.set('_output', reevaluate_output())
        res = {'ret_code': 0}
        if sig:
            sig.set_output(env.sos_dict['_output'])
            if sig.write():
                res.update({'output': sig.content['output'], 'shared': sig.content['end_context']})
        if capture_output:
            res.update({'stdout': outmsg, 'stderr': errmsg})
        return res
    except (StopInputGroup, TerminateExecution, UnknownTarget, RemovedTarget, UnavailableLock, PendingTasks) as e:
        res = {'ret_code': 1, 'exception': e}
        if capture_output:
            res.update({'stdout': outmsg, 'stderr': errmsg})
        return res
    except (KeyboardInterrupt, SystemExit) as e:
        # Note that KeyboardInterrupt is not an instance of Exception so this piece is needed for
        # the subprocesses to handle keyboard interrupt. We do not pass the exception
        # back to the master process because the master process would handle KeyboardInterrupt
        # as well and has no chance to handle the returned code.
        procs = psutil.Process().children(recursive=True)
        if procs:
            if env.verbosity > 2:
                env.logger.info(
                    f'{os.getpid()} interrupted. Killing subprocesses {" ".join(str(x.pid) for x in procs)}')
            for p in procs:
                p.terminate()
            gone, alive = psutil.wait_procs(procs, timeout=3)
            if alive:
                for p in alive:
                    p.kill()
            gone, alive = psutil.wait_procs(procs, timeout=3)
            if alive:
                for p in alive:
                    env.logger.warning(f'Failed to kill subprocess {p.pid}')
        elif env.verbosity > 2:
            env.logger.info(f'{os.getpid()} interrupted. No subprocess.')
        raise e
    except subprocess.CalledProcessError as e:
        # cannot pass CalledProcessError back because it is not pickleable
        res = {'ret_code': e.returncode, 'exception': RuntimeError(e.stderr)}
        if capture_output:
            res.update({'stdout': outmsg, 'stderr': errmsg})
        return res
    except ArgumentError as e:
        return {'ret_code': 1, 'exception': e}
    except Exception as e:
        error_class = e.__class__.__name__
        cl, exc, tb = sys.exc_info()
        msg = ''
        for st in reversed(traceback.extract_tb(tb)):
            if st.filename.startswith('script_'):
                code = stmtHash.script(st.filename)
                line_number = st.lineno
                code = '\n'.join([f'{"---->" if i+1 == line_number else "     "} {x.rstrip()}' for i,
                                  x in enumerate(code.splitlines())][max(line_number - 3, 0):line_number + 3])
                msg += f'''\
{st.filename} in {st.name}
{code}
'''
        detail = e.args[0] if e.args else ''
        res = {'ret_code': 1, 'exception': RuntimeError(f'''
---------------------------------------------------------------------------
{error_class:42}Traceback (most recent call last)
{msg}
{error_class}: {detail}''') if msg else RuntimeError(f'{error_class}: {detail}')}
        if capture_output:
            res.update({'stdout': outmsg, 'stderr': errmsg})
        return res
    finally:
        # release the lock even if the process becomes zombie? #871
        if sig:
            sig.release(quiet=True)

def verify_input():
    # now, if we are actually going to run the script, we
    # need to check the input files actually exists, not just the signatures
    for key in ('_input', '_depends'):
        for target in env.sos_dict[key]:
            if not target.target_exists('target'):
                raise RemovedTarget(target)

def expand_input_files(value, *args):
    # if unspecified, use __step_output__ as input (default)
    # resolve dynamic input.
    args = [x.resolve() if isinstance(x, dynamic) else x for x in args]
    if not args:
        return env.sos_dict['step_input']
    else:
        return _expand_file_list(False, *args)

def expand_depends_files(*args, **kwargs):
    '''handle directive depends'''
    args = [x.resolve() if isinstance(x, dynamic) else x for x in args]
    return _expand_file_list(False, *args)

def expand_output_files(value, *args):
    '''Process output files (perhaps a pattern) to determine input files.
    '''
    if any(isinstance(x, dynamic) for x in args):
        return sos_targets(undetermined=value)
    else:
        return _expand_file_list(True, *args)

def reevaluate_output():
    # re-process the output statement to determine output files
    args, _ = SoS_eval(
        f'__null_func__({env.sos_dict["step_output"]._undetermined})')
    if args is True:
        env.logger.error('Failed to resolve unspecified output')
        return
    # handle dynamic args
    args = [x.resolve() if isinstance(x, dynamic) else x for x in args]
    return expand_output_files('', *args)

def parse_shared_vars(option):
    shared_vars = set()
    if not option:
        return shared_vars
    if isinstance(option, str):
        shared_vars.add(option)
    elif isinstance(option, Mapping):
        for var, val in option.items():
            shared_vars |= accessed_vars(val)
    elif isinstance(option, Sequence):
        for item in option:
            if isinstance(item, str):
                shared_vars.add(item)
            elif isinstance(item, Mapping):
                for var, val in item.items():
                    shared_vars |= accessed_vars(val)
    return shared_vars

def evaluate_shared(vars, option):
    # handle option shared and store variables in a "__shared_vars" variable
    shared_vars = {}
    env.sos_dict.quick_update(vars[-1])
    for key in vars[-1].keys():
        try:
            if key in ('output', 'depends', 'input'):
                env.logger.warning(f'Cannot overwrite variable step_{key} from substep variable {key}')
            else:
                env.sos_dict.set('step_' + key, [x[key] for x in vars])
        except Exception as e:
            env.logger.warning('Failed to create step level variable step_{key}')
    if isinstance(option, str):
        if option in env.sos_dict:
            shared_vars[option] = env.sos_dict[option]
        else:
            raise RuntimeError(f'shared variable does not exist: {option}')
    elif isinstance(option, Mapping):
        for var, val in option.items():
            try:
                if var == val:
                    shared_vars[var] = env.sos_dict[var]
                else:
                    shared_vars[var] = SoS_eval(val)
            except Exception as e:
                raise RuntimeError(
                    f'Failed to evaluate shared variable {var} from expression {val}: {e}')
    # if there are dictionaries in the sequence, e.g.
    # shared=['A', 'B', {'C':'D"}]
    elif isinstance(option, Sequence):
        for item in option:
            if isinstance(item, str):
                if item in env.sos_dict:
                    shared_vars[item] = env.sos_dict[item]
                else:
                    raise RuntimeError(f'shared variable does not exist: {option}')
            elif isinstance(item, Mapping):
                for var, val in item.items():
                    try:
                        if var == val:
                            continue
                        else:
                            shared_vars[var] = SoS_eval(val)
                    except Exception as e:
                        raise RuntimeError(
                            f'Failed to evaluate shared variable {var} from expression {val}: {e}')
            else:
                raise RuntimeError(f'Unacceptable shared option. Only str or mapping are accepted in sequence: {option}')
    else:
        raise RuntimeError(f'Unacceptable shared option. Only str, sequence, or mapping are accepted in sequence: {option}')
    return shared_vars

class Base_Step_Executor:
    # This base class defines how steps are executed. The derived classes will reimplement
    # some function to behave differently in different modes.
    #
    def __init__(self, step):
        self.step = step
        self.task_manager = None

    def verify_output(self):
        if env.sos_dict['step_output'] is None:
            return
        if not env.sos_dict['step_output'].valid():
            raise RuntimeError(
                'Output of a completed step cannot be undetermined or unspecified.')
        for target in env.sos_dict['step_output']:
            if isinstance(target, sos_step):
                continue
            if isinstance(target, str):
                if not file_target(target).target_exists('any'):
                    if env.config['run_mode'] == 'dryrun':
                        # in dryrun mode, we just create these targets
                        file_target(target).create_placeholder()
                    else:
                        # latency wait for 5 seconds because the file system might be slow
                        time.sleep(5)
                        if not file_target(target).target_exists('any'):
                            raise RuntimeError(
                                f'Output target {target} does not exist after the completion of step {env.sos_dict["step_name"]} (curdir={os.getcwd()})')
            elif not target.target_exists('any'):
                if env.config['run_mode'] == 'dryrun':
                    target.create_placeholder()
                else:
                    time.sleep(5)
                    if not target.target_exists('any'):
                        raise RuntimeError(
                            f'Output target {target} does not exist after the completion of step {env.sos_dict["step_name"]}')

    # Nested functions to handle different parameters of input directive
    @staticmethod
    def handle_group_by(ifiles: sos_targets, group_by: Union[int, str]):
        '''Handle input option group_by'''
        if group_by == 'single':
            return [sos_targets(x) for x in ifiles]
        elif group_by == 'all':
            # default option
            return [sos_targets(ifiles)]
        elif group_by == 'pairs':
            if len(ifiles) % 2 != 0:
                raise ValueError(
                    f'Paired group_by has to have even number of input files: {len(ifiles)} provided')
            return list(sos_targets(x) for x in zip(ifiles[:len(ifiles) // 2], ifiles[len(ifiles) // 2:]))
        elif group_by == 'pairwise':
            f1, f2 = tee(ifiles)
            next(f2, None)
            return [sos_targets(x) for x in zip(f1, f2)]
        elif group_by == 'combinations':
            return [sos_targets(x) for x in combinations(ifiles, 2)]
        elif isinstance(group_by, int) or group_by.isdigit():
            group_by = int(group_by)
            if len(ifiles) % group_by != 0 and len(ifiles) > group_by:
                env.logger.warning(
                    f'Number of samples ({len(ifiles)}) is not a multiple of group_by ({group_by}). The last group would have less files than the other groups.')
            if group_by < 1:
                raise ValueError(
                    'Value of paramter group_by should be a positive number.')
            return [sos_targets(ifiles[i:i + group_by]) for i in range(0, len(ifiles), group_by)]
        else:
            raise ValueError(f'Unsupported group_by option ``{group_by}``!')

    @staticmethod
    def handle_paired_with(paired_with, ifiles: sos_targets, _groups: List[sos_targets], _vars: List[dict]):
        '''Handle input option paired_with'''
        if paired_with is None or not paired_with:
            var_name = []
            var_value = []
        elif isinstance(paired_with, str):
            var_name = ['_' + paired_with]
            if paired_with not in env.sos_dict:
                raise ValueError(f'Variable {paired_with} does not exist.')
            var_value = [env.sos_dict[paired_with]]
        elif isinstance(paired_with, dict):
            var_name = []
            var_value = []
            for k, v in paired_with.items():
                var_name.append(k)
                var_value.append(v)
        elif isinstance(paired_with, Iterable):
            try:
                var_name = ['_' + x for x in paired_with]
            except Exception:
                raise ValueError(
                    f'Invalud value for option paired_with {paired_with}')
            var_value = []
            for vn in var_name:
                if vn[1:] not in env.sos_dict:
                    raise ValueError(f'Variable {vn[1:]} does not exist.')
                var_value.append(env.sos_dict[vn[1:]])
        else:
            raise ValueError(
                f'Unacceptable value for parameter paired_with: {paired_with}')
        #
        for vn, vv in zip(var_name, var_value):
            if isinstance(vv, str) or not isinstance(vv, Iterable):
                raise ValueError(
                    f'paired_with variable {vn} is not a sequence ("{vv}")')
            if len(vv) != len(ifiles):
                raise ValueError(
                    f'Length of variable {vn} (length {len(vv)}) should match the number of input files (length {len(ifiles)}).')
            file_map = {x: y for x, y in zip(ifiles, vv)}
            for idx, grp in enumerate(_groups):
                mapped_vars = [file_map[x] for x in grp]
                # 862. we make the paired variable the same type so that if the input is a paths or sos_targets,
                # the returned value is of the same type
                _vars[idx][vn] = type(vv)(mapped_vars)

    @staticmethod
    def handle_group_with(group_with, ifiles: sos_targets, _groups: List[sos_targets], _vars: List[dict]):
        '''Handle input option group_with'''
        if group_with is None or not group_with:
            var_name = []
            var_value = []
        elif isinstance(group_with, str):
            var_name = ['_' + group_with]
            if group_with not in env.sos_dict:
                raise ValueError(f'Variable {group_with} does not exist.')
            var_value = [env.sos_dict[group_with]]
        elif isinstance(group_with, dict):
            var_name = []
            var_value = []
            for k, v in group_with.items():
                var_name.append(k)
                var_value.append(v)
        elif isinstance(group_with, Iterable):
            try:
                var_name = ['_' + x for x in group_with]
            except Exception:
                raise ValueError(
                    f'Invalud value for option group_with {group_with}')
            var_value = []
            for vn in var_name:
                if vn[1:] not in env.sos_dict:
                    raise ValueError(f'Variable {vn[1:]} does not exist.')
                var_value.append(env.sos_dict[vn[1:]])
        else:
            raise ValueError(
                f'Unacceptable value for parameter group_with: {group_with}')
        #
        for vn, vv in zip(var_name, var_value):
            if isinstance(vv, str) or not isinstance(vv, Iterable):
                raise ValueError(
                    f'group_with variable {vn} is not a sequence ("{vv}")')
            if len(vv) != len(_groups):
                raise ValueError(
                    f'Length of variable {vn} (length {len(vv)}) should match the number of input groups (length {len(_groups)}).')
            for idx, grp in enumerate(_groups):
                _vars[idx][vn] = vv[idx]

    @staticmethod
    def handle_extract_pattern(pattern, ifiles: sos_targets, _groups: List[sos_targets], _vars: List[dict]):
        '''Handle input option pattern'''
        if pattern is None or not pattern:
            patterns = []
        elif isinstance(pattern, str):
            patterns = [pattern]
        elif isinstance(pattern, Iterable):
            patterns = pattern
        else:
            raise ValueError(
                f'Unacceptable value for parameter pattern: {pattern}')
        #
        for pattern in patterns:
            res = extract_pattern(pattern, ifiles)
            # now, assign the variables to env
            for k, v in res.items():
                if k in ('step_input', 'step_output', 'step_depends') or k.startswith('_'):
                    raise RuntimeError(
                        f'Pattern defined variable {k} is not allowed')
                env.sos_dict[k] = v
            # also make k, v pair with _input
            Base_Step_Executor.handle_paired_with(
                res.keys(), ifiles, _groups, _vars)

    @staticmethod
    def handle_for_each(for_each, _groups: List[sos_targets], _vars: List[dict]):
        if for_each is None or not for_each:
            for_each = []
        elif isinstance(for_each, (str, dict)):
            for_each = [for_each]
        elif isinstance(for_each, Sequence):
            for_each = for_each
        else:
            raise ValueError(
                f'Unacceptable value for parameter for_each: {for_each}')
        #
        for fe_all in for_each:
            if isinstance(fe_all, dict):
                # in the format of {'name': value}
                fe_iter_names = []
                fe_values = []
                for k, v in fe_all.items():
                    if ',' in k:
                        names = [x.strip() for x in k.split(',')]
                        if isinstance(v, Iterable):
                            v = list(v)
                        if any(len(_v) != len(names) for _v in v):
                            raise ValueError(
                                f'Unable to unpack object {short_repr(v)} for variables {k} (of length {len(names)})')
                        fe_iter_names.extend(names)
                        fe_values.extend(list(zip(*v)))
                    else:
                        fe_iter_names.append(k)
                        fe_values.append(v)
            else:
                if ',' in fe_all:
                    fe_var_names = [x.strip() for x in fe_all.split(',')]
                    fe_iter_names = ['_' + x for x in fe_var_names]
                else:
                    fe_var_names = [fe_all]
                    fe_iter_names = ['_' + fe_all]
                # check iterator variable name
                for name in fe_iter_names:
                    if '.' in name:
                        raise ValueError(f'Invalid iterator variable {name}')
                # check variables
                fe_values = []
                for name in fe_var_names:
                    if name.split('.')[0] not in env.sos_dict:
                        raise ValueError(f'Variable {name} does not exist.')
                    if '.' in name:
                        fe_values.append(
                            getattr(env.sos_dict[name.split('.')[0]], name.split('.', 1)[-1]))
                    else:
                        fe_values.append(env.sos_dict[name])

            # get loop size
            loop_size = None
            for name, values in zip(fe_iter_names, fe_values):
                if not isinstance(values, Sequence):
                    try:
                        import pandas as pd
                        if not isinstance(values, (pd.DataFrame, pd.Series, pd.Index)):
                            raise ValueError(
                                f'Unacceptable for_each data type {values.__class__.__name__}')
                    except Exception as e:
                        raise ValueError(
                            f'Cannot iterate through variable {name}: {e}')
                if loop_size is None:
                    loop_size = len(values)
                elif loop_size != len(values):
                    raise ValueError(
                        f'Length of variable {name} (length {len(values)}) should match the length of other variables (length {loop_size}).')
            # expand
            _tmp_groups = copy.deepcopy(_groups)
            _groups.clear()
            for _ in range(loop_size):
                _groups.extend(_tmp_groups)
            #
            _tmp_vars = copy.deepcopy(_vars)
            _vars.clear()
            for vidx in range(loop_size):
                for idx, _ in enumerate(_tmp_vars):
                    for var_name, values in zip(fe_iter_names, fe_values):
                        if isinstance(values, Sequence):
                            _tmp_vars[idx][var_name] = values[vidx]
                        elif isinstance(values, (pd.DataFrame, pd.Series)):
                            _tmp_vars[idx][var_name] = values.iloc[vidx]
                        elif isinstance(values, pd.Index):
                            _tmp_vars[idx][var_name] = values[vidx]
                        else:
                            raise ValueError(
                                f'Failed to iterate through for_each variable {short_repr(values)}')
                _vars.extend(copy.deepcopy(_tmp_vars))

    # directive input
    def process_input_args(self, ifiles: sos_targets, **kwargs):
        """This function handles directive input and all its parameters.
        It
            determines and set __step_input__
            determines and set pattern variables if needed
        returns
            _groups
            _vars
        which are groups of _input and related _vars
        """
        if ifiles.unspecified():
            env.sos_dict.set('step_input', sos_targets([]))
            env.sos_dict.set('_input', sos_targets([]))
            env.sos_dict.set('step_output', sos_targets())
            return [sos_targets([])], [{}]

        for k in kwargs.keys():
            if k not in SOS_INPUT_OPTIONS:
                raise RuntimeError(f'Unrecognized input option {k}')
        #
        if 'filetype' in kwargs:
            if isinstance(kwargs['filetype'], str):
                ifiles = fnmatch.filter(ifiles.targets(
                    file_only=True), kwargs['filetype'])
            elif isinstance(kwargs['filetype'], Iterable):
                ifiles = [x for x in ifiles.targets(file_only=True) if any(fnmatch.fnmatch(x, y)
                                                                           for y in kwargs['filetype'])]
            elif callable(kwargs['filetype']):
                ifiles = [x for x in ifiles.targets(
                    file_only=True) if kwargs['filetype'](x)]
        #
        # input file is the filtered files
        env.sos_dict.set('step_input', sos_targets(ifiles))
        env.sos_dict.set('_input', sos_targets(ifiles))
        #
        # handle group_by
        if 'group_by' in kwargs:
            _groups = Base_Step_Executor.handle_group_by(
                sos_targets(ifiles), kwargs['group_by'])
            if not _groups:
                env.logger.debug('No group defined because of no input file')
                _groups = [sos_targets([])]
        else:
            _groups = [sos_targets(ifiles)]
        #
        _vars = [{} for x in _groups]
        # handle paired_with
        if 'paired_with' in kwargs:
            Base_Step_Executor.handle_paired_with(
                kwargs['paired_with'], ifiles,  _groups, _vars)
        # handle pattern
        if 'pattern' in kwargs:
            Base_Step_Executor.handle_extract_pattern(
                kwargs['pattern'], ifiles, _groups, _vars)
        # handle group_with
        if 'group_with' in kwargs:
            Base_Step_Executor.handle_group_with(
                kwargs['group_with'], ifiles,  _groups, _vars)
        # handle for_each
        if 'for_each' in kwargs:
            Base_Step_Executor.handle_for_each(
                kwargs['for_each'], _groups, _vars)
        return _groups, _vars

    def process_depends_args(self, dfiles: sos_targets, **kwargs):
        for k in kwargs.keys():
            if k not in SOS_DEPENDS_OPTIONS:
                raise RuntimeError(f'Unrecognized depends option {k}')
        if dfiles.undetermined():
            raise ValueError(r"Depends needs to handle undetermined")

        env.sos_dict.set('_depends', dfiles)
        if env.sos_dict['step_depends'] is None:
            env.sos_dict.set('step_depends', dfiles)
        # dependent files can overlap
        elif env.sos_dict['step_depends'].targets() != dfiles:
            env.sos_dict['step_depends'].extend(dfiles)

    def process_output_args(self, ofiles: sos_targets, **kwargs):
        for k in kwargs.keys():
            if k not in SOS_OUTPUT_OPTIONS:
                raise RuntimeError(f'Unrecognized output option {k}')
        if 'group_by' in kwargs:
            _ogroups = Base_Step_Executor.handle_group_by(
                ofiles, kwargs['group_by'])
            if len(_ogroups) != len(self._substeps):
                raise RuntimeError(
                    f'Output option group_by produces {len(_ogroups)} output groups which is different from the number of input groups ({len(self._substeps)}).')
            ofiles = _ogroups[env.sos_dict['_index']]

        # create directory
        if ofiles.valid():
            for ofile in ofiles:
                if isinstance(ofile, file_target):
                    parent_dir = ofile.parent
                    if parent_dir and not parent_dir.is_dir():
                        parent_dir.mkdir(parents=True, exist_ok=True)

        # set variables
        env.sos_dict.set('_output', ofiles)
        #
        if not env.sos_dict['step_output'].valid():
            env.sos_dict.set('step_output', copy.deepcopy(ofiles))
        else:
            for ofile in ofiles:
                if ofile in env.sos_dict['step_output']._targets:
                    raise ValueError(
                        f'Output {ofile} from substep {env.sos_dict["_index"]} overlaps with output from a previous substep')
            env.sos_dict['step_output'].extend(ofiles)

    def process_task_args(self, **kwargs):
        env.sos_dict.set('_runtime', {})
        for k, v in kwargs.items():
            if k not in SOS_RUNTIME_OPTIONS:
                raise RuntimeError(f'Unrecognized runtime option {k}={v}')
            # standardize walltime to an integer
            if k == 'walltime':
                v = format_HHMMSS(v)
            elif k == 'mem':
                v = expand_size(v)
            env.sos_dict['_runtime'][k] = v

    def prepare_task(self):
        env.sos_dict['_runtime']['cur_dir'] = os.getcwd()
        # we need to record the verbosity and sigmode of task during creation because
        # they might be changed while the task is in the queue waiting to be
        # submitted (this happens when tasks are submitted from Jupyter)
        env.sos_dict['_runtime']['verbosity'] = env.verbosity
        env.sos_dict['_runtime']['sig_mode'] = env.config.get(
            'sig_mode', 'default')
        env.sos_dict['_runtime']['run_mode'] = env.config.get(
            'run_mode', 'run')
        env.sos_dict['_runtime']['home_dir'] = os.path.expanduser('~')
        if 'workdir' in env.sos_dict['_runtime'] and not os.path.isdir(os.path.expanduser(env.sos_dict['_runtime']['workdir'])):
            try:
                os.makedirs(os.path.expanduser(
                    env.sos_dict['_runtime']['workdir']))
            except Exception:
                raise RuntimeError(
                    f'Failed to create workdir {env.sos_dict["_runtime"]["workdir"]}')

        # NOTE: we do not explicitly include 'step_input', 'step_output',
        # 'step_depends' and 'CONFIG'
        # because they will be included by env.sos_dict['__signature_vars__'] if they are actually
        # used in the task. (issue #752)
        task_vars = env.sos_dict.clone_selected_vars(env.sos_dict['__signature_vars__']
                                                     | {'_input', '_output', '_depends', '_index', '__args__', 'step_name', '_runtime',
                                                        '__signature_vars__', '__step_context__'
                                                        })

        task_tags = [env.sos_dict['step_name'], env.sos_dict['workflow_id']]
        if 'tags' in env.sos_dict['_runtime']:
            if isinstance(env.sos_dict['_runtime']['tags'], str):
                tags = [env.sos_dict['_runtime']['tags']]
            elif isinstance(env.sos_dict['_runtime']['tags'], Sequence):
                tags = list(env.sos_dict['_runtime']['tags'])
            else:
                env.logger.warning(
                    f'Unacceptable value for parameter tags: {env.sos_dict["_runtime"]["tags"]}')
            #
            for tag in tags:
                if not tag.strip():
                    continue
                if not SOS_TAG.match(tag):
                    new_tag = re.sub(r'[^\w_.-]', '', tag)
                    if new_tag:
                        env.logger.warning(
                            f'Invalid tag "{tag}" is added as "{new_tag}"')
                        task_tags.append(new_tag)
                    else:
                        env.logger.warning(f'Invalid tag "{tag}" is ignored')
                else:
                    task_tags.append(tag)

        # save task to a file
        task_vars['__task_vars__'] = copy.copy(task_vars)
        taskdef = TaskParams(
            name='{} (index={})'.format(
                self.step.step_name(), env.sos_dict['_index']),
            global_def=self.step.global_def,
            task=self.step.task,          # task
            sos_dict=task_vars,
            tags=task_tags
        )
        # if no output (thus no signature)
        # temporarily create task signature to obtain sig_id
        task_id = RuntimeInfo(self.step.md5, self.step.task, task_vars['_input'],
                              task_vars['_output'], task_vars['_depends'],
                              task_vars['__signature_vars__'], task_vars).sig_id

        # workflow ID should be included but not part of the signature, this is why it is included
        # after task_id is created.
        task_vars['workflow_id'] = env.sos_dict['workflow_id']

        if self.task_manager is None:
            if 'trunk_size' in env.sos_dict['_runtime']:
                if not isinstance(env.sos_dict['_runtime']['trunk_size'], int):
                    raise ValueError(
                        f'An integer value is expected for runtime option trunk, {env.sos_dict["_runtime"]["trunk_size"]} provided')
                trunk_size = env.sos_dict['_runtime']['trunk_size']
            else:
                trunk_size = 1
            if 'trunk_workers' in env.sos_dict['_runtime']:
                if not isinstance(env.sos_dict['_runtime']['trunk_workers'], int):
                    raise ValueError(
                        f'An integer value is expected for runtime option trunk_workers, {env.sos_dict["_runtime"]["trunk_workers"]} provided')
                trunk_workers = env.sos_dict['_runtime']['trunk_workers']
            else:
                trunk_workers = 0

            # if 'queue' in env.sos_dict['_runtime'] and env.sos_dict['_runtime']['queue']:
            #    host = env.sos_dict['_runtime']['queue']
            # else:
            #    # otherwise, use workflow default
            #    host = '__default__'

            self.task_manager = TaskManager(trunk_size, trunk_workers)

        # 618
        # it is possible that identical tasks are executed (with different underlying random numbers)
        # we should either give a warning or produce different ids...
        if self.task_manager.has_task(task_id):
            raise RuntimeError(
                f'Identical task {task_id} generated from _index={env.sos_dict["_index"]}.')
        elif self.task_manager.has_output(task_vars['_output']):
            raise RuntimeError(
                f'Task produces output files {", ".join(task_vars["_output"])} that are output of other tasks.')
        # if no trunk_size, the job will be submitted immediately
        # otherwise tasks will be accumulated and submitted in batch
        self.task_manager.append(
            (task_id, taskdef, task_vars['_output'].targets()))
        tasks = self.task_manager.get_job()
        if tasks:
            self.submit_tasks(tasks)
        return task_id

    def wait_for_results(self):
        if self.concurrent_substep:
            sm = SlotManager()
            nMax = env.config.get(
                'max_procs', max(int(os.cpu_count() / 2), 1))
            if nMax > self.worker_pool._processes - 1 and len(self._substeps) > nMax:
                # use billiard pool, can expand pool if more slots are available
                while True:
                    nPending = [not x.ready()
                                for x in self.proc_results].count(True)
                    if nPending == 0:
                        self.proc_results = [x.get()
                                             for x in self.proc_results]
                        break
                    if sm.available(nMax) > 0:
                        extra = sm.acquire(nPending - 1, nMax)
                        if extra > 0:
                            self.worker_pool.grow(extra)
                            env.logger.debug(f'Expand pool by {extra} slots')
                    time.sleep(1)
            else:
                self.proc_results = [x.get() for x in self.proc_results]
            sm.release(self.worker_pool._processes - 1)
            self.worker_pool.close()
            self.worker_pool.join()
            self.worker_pool = None
            return

        if self.task_manager is None:
            return {}

        # submit the last batch of tasks
        tasks = self.task_manager.get_job(all_tasks=True)
        if tasks:
            self.submit_tasks(tasks)

        # waiting for results of specified IDs
        results = self.wait_for_tasks(self.task_manager._submitted_tasks)
        #
        # report task
        # what we should do here is to get the alias of the Host
        # because it can be different (e.g. not localhost
        if 'queue' in env.sos_dict['_runtime'] and env.sos_dict['_runtime']['queue']:
            queue = env.sos_dict['_runtime']['queue']
        elif env.config['default_queue']:
            queue = env.config['default_queue']
        else:
            queue = 'localhost'

        for id, result in results.items():
            # turn to string to avoid naming lookup issue
            rep_result = {x: (y if isinstance(y, (int, bool, float, str)) else short_repr(
                y)) for x, y in result.items()}
            rep_result['tags'] = ' '.join(self.task_manager.tags(id))
            rep_result['queue'] = queue
            workflow_signatures.write('task', id, repr(rep_result))
        self.task_manager.clear_submitted()

        # if in dryrun mode, we display the output of the dryrun task
        if env.config['run_mode'] == 'dryrun':
            tid = list(results.keys())[0]
            tf = TaskFile(tid)
            if tf.has_stdout():
                print(TaskFile(tid).stdout)

        for idx, task in enumerate(self.proc_results):
            # if it is done
            if isinstance(task, dict):
                continue
            if task in results:
                self.proc_results[idx] = results[task]
            else:
                # can be a subtask
                for _, mres in results.items():
                    if 'subtasks' in mres and task in mres['subtasks']:
                        self.proc_results[idx] = mres['subtasks'][task]
        #
        # check if all have results?
        if any(isinstance(x, str) for x in self.proc_results):
            raise RuntimeError(
                f'Failed to get results for tasks {", ".join(x for x in self.proc_results if isinstance(x, str))}')
        #
        for idx, res in enumerate(self.proc_results):
            if 'skipped' in res:
                if res['skipped']:
                    self.completed['__task_skipped__'] += 1
                else:
                    self.completed['__task_completed__'] += 1
            if 'shared' in res:
                self.shared_vars[idx].update(res['shared'])

    def log(self, stage=None, msg=None):
        if stage == 'start':
            env.logger.info(
                f'{"Checking" if env.config["run_mode"] == "dryrun" else "Running"} ``{self.step.step_name(True)}``: {self.step.comment.strip()}')
        elif stage == 'input statement':
            env.logger.trace(f'Handling input statement {msg}')
        elif stage == '_input':
            if env.sos_dict['_input'] is not None:
                env.logger.debug(
                    f'_input: ``{short_repr(env.sos_dict["_input"])}``')
        elif stage == '_depends':
            if env.sos_dict['_depends'] is not None:
                env.logger.debug(
                    f'_depends: ``{short_repr(env.sos_dict["_depends"])}``')
        elif stage == 'input':
            if env.sos_dict['step_input'] is not None:
                env.logger.info(
                    f'input:   ``{short_repr(env.sos_dict["step_input"])}``')
        elif stage == 'output':
            if env.sos_dict['step_output'] is not None and len(env.sos_dict['step_output']) > 0:
                env.logger.info(
                    f'output:   ``{short_repr(env.sos_dict["step_output"])}``')

    def execute(self, stmt):
        try:
            self.last_res = SoS_exec(
                stmt, return_result=self.run_mode == 'interactive')
        except (StopInputGroup, TerminateExecution, UnknownTarget, RemovedTarget, UnavailableLock, PendingTasks):
            raise
        except subprocess.CalledProcessError as e:
            raise RuntimeError(e.stderr)
        except ArgumentError:
            raise
        except Exception as e:
            error_class = e.__class__.__name__
            cl, exc, tb = sys.exc_info()
            msg = ''
            for st in reversed(traceback.extract_tb(tb)):
                if st.filename.startswith('script_'):
                    code = stmtHash.script(st.filename)
                    line_number = st.lineno
                    code = '\n'.join([f'{"---->" if i+1 == line_number else "     "} {x.rstrip()}' for i,
                                      x in enumerate(code.splitlines())][max(line_number - 3, 0):line_number + 3])
                    msg += f'''\
{st.filename} in {st.name}
{code}
'''
            detail = e.args[0] if e.args else ''
            if msg:
                raise RuntimeError(f'''
---------------------------------------------------------------------------
{error_class:42}Traceback (most recent call last)
{msg}
{error_class}: {detail}''')
            else:
                raise RuntimeError(f'{error_class}: {detail}')

    def collect_result(self):
        # only results will be sent back to the master process
        #
        # __step_input__:    input of this step
        # __steo_output__:   output of this step
        # __step_depends__:  dependent files of this step
        result = {
            '__step_input__': env.sos_dict['step_input'],
            '__step_output__': env.sos_dict['step_output'],
            '__step_depends__': env.sos_dict['step_depends'],
            '__step_name__': env.sos_dict['step_name'],
            '__completed__': self.completed,
        }
        result['__last_res__'] = self.last_res
        result['__changed_vars__'] = set()
        result['__shared__'] = {}
        if 'shared' in self.step.options:
            result['__shared__'] = self.shared_vars
        if hasattr(env, 'accessed_vars'):
            result['__environ_vars__'] = self.environ_vars
            result['__signature_vars__'] = env.accessed_vars
        return result

    def run(self):
        '''Execute a single step and return results. The result for batch mode is the
        input, output etc returned as alias, and for interactive mode is the return value
        of the last expression. '''
        # return value of the last executed statement
        self.last_res = None
        self.start_time = time.time()
        self.completed = defaultdict(int)
        #
        # prepare environments, namely variables that can be used by the step
        #
        # * step_name:  name of the step, can be used by step process to determine
        #               actions dynamically.
        env.sos_dict.set('step_name', self.step.step_name())
        self.log('start')
        env.sos_dict.set('step_id', self.step.md5)
        # used by nested workflow
        env.sos_dict.set('__step_context__', self.step.context)

        env.sos_dict.set('_runtime', {})
        # * input:      input files, which should be __step_output__ if it is defined, or
        #               None otherwise.
        # * _input:     first batch of input, which should be input if no input statement is used
        # * output:     None at first, can be redefined by output statement
        # * _output:    None at first, can be redefined by output statement
        # * depends:    None at first, can be redefined by depends statement
        # * _depends:   None at first, can be redefined by depends statement
        #
        if '__step_output__' not in env.sos_dict or env.sos_dict['__step_output__'].unspecified():
            env.sos_dict.set('step_input', sos_targets([]))
        else:
            env.sos_dict.set('step_input', env.sos_dict['__step_output__'])

        # input can be Undetermined from undetermined output from last step
        env.sos_dict.set('_input', copy.deepcopy(env.sos_dict['step_input']))

        if '__default_output__' in env.sos_dict:
            # if step is triggered by sos_step, it should not be considered as
            # output of the step. #981
            env.sos_dict.set('__default_output__', sos_targets(
                [x for x in env.sos_dict['__default_output__']._targets
                 if not isinstance(x, sos_step)]))
            env.sos_dict.set('step_output', copy.deepcopy(
                env.sos_dict['__default_output__']))
            env.sos_dict.set('_output', copy.deepcopy(
                env.sos_dict['__default_output__']))
        else:
            env.sos_dict.set('step_output', sos_targets([]))
            # output is said to be unspecified until output: is used
            env.sos_dict.set('_output', sos_targets(undetermined=True))
        env.sos_dict.set('step_depends', sos_targets([]))
        env.sos_dict.set('_depends', sos_targets([]))
        # _index is needed for pre-input action's active option and for debug output of scripts
        env.sos_dict.set('_index', 0)

        env.logger.trace(
            f'Executing {env.sos_dict["step_name"]} with step_input {env.sos_dict["step_input"]} and step_output {env.sos_dict["step_output"]}')

        # look for input statement.
        input_statement_idx = [idx for idx, x in enumerate(
            self.step.statements) if x[0] == ':' and x[1] == 'input']
        if not input_statement_idx:
            input_statement_idx = None
        elif len(input_statement_idx) == 1:
            input_statement_idx = input_statement_idx[0]
        else:
            raise ValueError(
                f'More than one step input are specified in step {self.step.step_name()}')

        # if there is an input statement, execute the statements before it, and then the input statement
        self.concurrent_substep = False
        if input_statement_idx is not None:
            # execute before input stuff
            for statement in self.step.statements[:input_statement_idx]:
                if statement[0] == ':':
                    key, value = statement[1:3]
                    if key != 'depends':
                        raise ValueError(
                            f'Step input should be specified before {key}')
                    try:
                        args, kwargs = SoS_eval(f'__null_func__({value})')
                        dfiles = expand_depends_files(*args)
                        # dfiles can be Undetermined
                        self.process_depends_args(dfiles, **kwargs)
                    except (UnknownTarget, RemovedTarget, UnavailableLock):
                        raise
                    except Exception as e:
                        raise RuntimeError(
                            f'Failed to process step {key} ({value.strip()}): {e}')
                else:
                    try:
                        self.execute(statement[1])
                    except StopInputGroup as e:
                        if e.message:
                            env.logger.warning(e)
                        return self.collect_result()
            # input statement
            stmt = self.step.statements[input_statement_idx][2]
            self.log('input statement', stmt)
            try:
                args, kwargs = SoS_eval(f"__null_func__({stmt})")
                # Files will be expanded differently with different running modes
                input_files: sos_targets = expand_input_files(stmt, *args)
                self._substeps, self._vars = self.process_input_args(
                    input_files, **kwargs)
                #
                # if shared is true, we have to disable concurrent because we
                # do not yet return anything from shared.
                self.concurrent_substep = 'concurrent' in kwargs and kwargs['concurrent'] and len(
                    self._substeps) > 1 and self.run_mode != 'dryrun'
            except (UnknownTarget, RemovedTarget, UnavailableLock):
                raise
            except Exception as e:
                raise ValueError(
                    f'Failed to process input statement {stmt}: {e}')

            input_statement_idx += 1
        else:
            # default case
            self._substeps = [env.sos_dict['step_input']]
            self._vars = [{}]
            # assuming everything starts from 0 is after input
            input_statement_idx = 0

        self.proc_results = []
        self.vars_to_be_shared = set()
        if 'shared' in self.step.options:
            self.vars_to_be_shared = parse_shared_vars(self.step.options['shared'])
        self.vars_to_be_shared = sorted([x[5:] if x.startswith('step_') else x for x in self.vars_to_be_shared if x not in ('step_', 'step_input', 'step_output', 'step_depends')])
        self.shared_vars = [{} for x in self._substeps]
        # run steps after input statement, which will be run multiple times for each input
        # group.
        env.sos_dict.set('__num_groups__', len(self._substeps))

        # determine if a single index or the whole step should be skipped
        skip_index = False
        # signatures of each index, which can remain to be None if no output
        # is defined.
        self.output_groups = [[] for x in self._substeps]

        if self.concurrent_substep:
            if self.step.task:
                # and 'concurrent' in env.sos_dict['_runtime'] and \
                #env.sos_dict['_runtime']['concurrent'] is False:
                self.concurrent_substep = False
                env.logger.debug(
                    'Input groups are executed sequentially because of existence of tasks')
            elif len([
                    x for x in self.step.statements[input_statement_idx:] if x[0] != ':']) > 1:
                self.concurrent_substep = False
                env.logger.debug(
                    'Input groups are executed sequentially because of existence of directives between statements.')
            elif any('sos_run' in x[1] for x in self.step.statements[input_statement_idx:]):
                self.concurrent_substep = False
                env.logger.debug(
                    'Input groups are executed sequentially because of existence of nested workflow.')
            else:
                sm = SlotManager()
                # because the master process pool will count one worker in (step)
                gotten = sm.acquire(len(self._substeps) - 1,
                                    env.config.get('max_procs', max(int(os.cpu_count() / 2), 1)))
                env.logger.debug(
                    f'Using process pool with size {gotten+1}')
                self.worker_pool = Pool(gotten + 1)

        try:
            self.completed['__substep_skipped__'] = 0
            self.completed['__substep_completed__'] = len(self._substeps)
            # pending signatures are signatures for steps with external tasks
            pending_signatures = [None for x in self._substeps]
            for idx, (g, v) in enumerate(zip(self._substeps, self._vars)):
                # other variables
                #
                env.sos_dict.update(v)
                env.sos_dict.set('_input', copy.deepcopy(g))

                self.log('_input')
                env.sos_dict.set('_index', idx)

                # in interactive mode, because sos_dict are always shared
                # execution of a substep, especially when it calls a nested
                # workflow, would change step_name, __step_context__ etc, and
                # we will have to reset these variables to make sure the next
                # substep would execute normally. Batch mode is immune to this
                # problem because nested workflows are executed in their own
                # process/context etc
                if env.config['run_mode'] == 'interactive':
                    env.sos_dict.set('step_name', self.step.step_name())
                    env.sos_dict.set('step_id', self.step.md5)
                    # used by nested workflow
                    env.sos_dict.set('__step_context__', self.step.context)
                #
                pre_statement = []
                if not any(st[0] == ':' and st[1] == 'output' for st in self.step.statements[input_statement_idx:]) and \
                        '__default_output__' in env.sos_dict:
                    pre_statement = [[':', 'output', '_output']]

                for statement in pre_statement + self.step.statements[input_statement_idx:]:
                    # if input is undertermined, we can only process output:
                    if not g.valid() and statement[0] != ':':
                        raise RuntimeError('Undetermined input encountered')
                        return self.collect_result()
                    if statement[0] == ':':
                        key, value = statement[1:3]
                        # output, depends, and process can be processed multiple times
                        try:
                            args, kwargs = SoS_eval(f'__null_func__({value})')
                            # dynamic output or dependent files
                            if key == 'output':
                                # if output is defined, its default value needs to be cleared
                                if idx == 0:
                                    env.sos_dict.set(
                                        'step_output', sos_targets())
                                ofiles: sos_targets = expand_output_files(value, *args)
                                if g.valid() and ofiles.valid():
                                    if any(x in g._targets for x in ofiles if not isinstance(x, sos_step)):
                                        raise RuntimeError(
                                            f'Overlapping input and output files: {", ".join(repr(x) for x in ofiles if x in g)}')
                                # set variable _output and output
                                self.process_output_args(ofiles, **kwargs)
                                self.output_groups[idx] = env.sos_dict['_output'].targets(
                                )
                            elif key == 'depends':
                                try:
                                    dfiles = expand_depends_files(*args)
                                    # dfiles can be Undetermined
                                    self.process_depends_args(dfiles, **kwargs)
                                    self.log('_depends')
                                except Exception as e:
                                    env.logger.info(e)
                                    raise
                            elif key == 'task':
                                self.process_task_args(*args, **kwargs)
                            else:
                                raise RuntimeError(
                                    f'Unrecognized directive {key}')
                        except (UnknownTarget, RemovedTarget, UnavailableLock):
                            raise
                        except Exception as e:
                            # if input is Undertermined, it is possible that output cannot be processed
                            # due to that, and we just return
                            if not g.valid():
                                env.logger.debug(e)
                                return self.collect_result()
                            raise RuntimeError(
                                f'Failed to process step {key} ({value.strip()}): {e}')
                    else:
                        try:
                            if self.concurrent_substep:
                                env.logger.trace(f'Execute substep {env.sos_dict["step_name"]} concurrently')

                                proc_vars = env.sos_dict.clone_selected_vars(
                                    env.sos_dict['__signature_vars__']
                                    | {'step_output', '_input', '_output', '_depends', '_index', '__args__',
                                       'step_name', '_runtime',
                                       '__signature_vars__', '__step_context__'
                                       })

                                self.proc_results.append(
                                    self.worker_pool.apply_async(concurrent_execute,
                                                                 kwds=dict(stmt=statement[1],
                                                                           proc_vars=proc_vars,
                                                                           step_md5=self.step.md5,
                                                                           step_tokens=self.step.tokens,
                                                                           shared_vars=self.vars_to_be_shared,
                                                                           capture_output=self.run_mode == 'interactive')))
                            else:
                                if env.config['sig_mode'] == 'ignore' or env.sos_dict['_output'].unspecified():
                                    env.logger.trace('Execute substep {env.sos_dict["step_name"]} without signature')
                                    verify_input()
                                    self.execute(statement[1])
                                    if 'shared' in self.step.options:
                                        try:
                                            self.shared_vars[env.sos_dict['_index']].update({
                                                x:env.sos_dict[x] for x in self.vars_to_be_shared
                                                    if x in env.sos_dict})
                                        except Exception as e:
                                            raise ValueError(f'Missing shared variable {e}.')
                                else:
                                    sig = RuntimeInfo(
                                        self.step.md5, self.step.tokens,
                                        env.sos_dict['_input'],
                                        env.sos_dict['_output'],
                                        env.sos_dict['_depends'],
                                        env.sos_dict['__signature_vars__'],
                                        shared_vars=self.vars_to_be_shared)
                                    env.logger.trace(f'Execute substep {env.sos_dict["step_name"]} with signature {sig.sig_id}')
                                    # if singaure match, we skip the substep even  if
                                    # there are tasks.
                                    matched = validate_step_sig(sig)
                                    skip_index = bool(matched)
                                    if matched:
                                        if env.sos_dict['step_output'].undetermined():
                                            self.output_groups[env.sos_dict['_index']] = matched["output"]
                                        if 'vars' in matched:
                                            self.shared_vars[env.sos_dict['_index']].update(matched["vars"])
                                    else:
                                        sig.lock()
                                        try:
                                            verify_input()
                                            self.execute(statement[1])
                                            if 'shared' in self.step.options:
                                                try:
                                                    self.shared_vars[env.sos_dict['_index']].update({
                                                        x:env.sos_dict[x] for x in self.vars_to_be_shared
                                                            if x in env.sos_dict})
                                                except Exception as e:
                                                    raise ValueError(f'Missing shared variable {e}.')
                                        finally:
                                            # if this is the end of substep, save the signature
                                            # otherwise we need to wait for the completion
                                            # of the task.
                                            if not self.step.task:
                                                if env.sos_dict['step_output'].undetermined():
                                                    output = reevaluate_output()
                                                    self.output_groups[env.sos_dict['_index']] = output
                                                    sig.set_output(output)
                                                sig.write()
                                            else:
                                                pending_signatures[idx] = sig
                                            sig.release()


                        except StopInputGroup as e:
                            self.output_groups[idx] = []
                            if e.message:
                                env.logger.info(e)
                            skip_index = True
                            break

                # if there is no statement , but there are tasks, we should
                # check signature here.
                if not any(x[0] == '!' for x in self.step.statements[input_statement_idx:]) and self.step.task \
                    and env.config['sig_mode'] != 'ignore' and not env.sos_dict['_output'].unspecified():
                    sig = RuntimeInfo(
                        self.step.md5, self.step.tokens,
                        env.sos_dict['_input'],
                        env.sos_dict['_output'],
                        env.sos_dict['_depends'],
                        env.sos_dict['__signature_vars__'],
                        shared_vars=self.vars_to_be_shared)
                    env.logger.trace(f'Check task-only step {env.sos_dict["step_name"]} with signature {sig.sig_id}')
                    matched = validate_step_sig(sig)
                    skip_index = bool(matched)
                    if matched:
                        if env.sos_dict['step_output'].undetermined():
                            self.output_groups[env.sos_dict['_index']] = matched["output"]
                        self.shared_vars[env.sos_dict['_index']].update(matched["vars"])
                    pending_signatures[idx] = sig

                # if this index is skipped, go directly to the next one
                if skip_index:
                    self.completed['__substep_skipped__'] += 1
                    self.completed['__substep_completed__'] -= 1
                    skip_index = False
                    continue

                # if concurrent input group, there is no task
                if self.concurrent_substep:
                    continue
                # finally, tasks..
                if not self.step.task:
                    continue

                if env.config['run_mode'] == 'dryrun' and env.sos_dict['_index'] != 0:
                    continue

                # check if the task is active
                if 'active' in env.sos_dict['_runtime']:
                    active = env.sos_dict['_runtime']['active']
                    if active is True:
                        pass
                    elif active is False:
                        continue
                    elif isinstance(active, int):
                        if active >= 0 and env.sos_dict['_index'] != active:
                            continue
                        if active < 0 and env.sos_dict['_index'] != active + env.sos_dict['__num_groups__']:
                            continue
                    elif isinstance(active, Sequence):
                        allowed_index = list(
                            [x if x >= 0 else env.sos_dict['__num_groups__'] + x for x in active])
                        if env.sos_dict['_index'] not in allowed_index:
                            continue
                    elif isinstance(active, slice):
                        allowed_index = list(
                            range(env.sos_dict['__num_groups__']))[active]
                        if env.sos_dict['_index'] not in allowed_index:
                            continue
                    else:
                        raise RuntimeError(
                            f'Unacceptable value for option active: {active}')

                #
                self.log('task')
                try:
                    task = self.prepare_task()
                    self.proc_results.append(task)
                except Exception as e:
                    # FIXME: cannot catch exception from subprocesses
                    if env.verbosity > 2:
                        sys.stderr.write(get_traceback())
                    raise RuntimeError(
                        f'Failed to execute process\n"{short_repr(self.step.task)}"\n{e}')
                #
                # if not concurrent, we have to wait for the completion of the task
                if 'concurrent' in env.sos_dict['_runtime'] and env.sos_dict['_runtime']['concurrent'] is False:
                    self.wait_for_results()
                #
                # endfor loop for each input group
                #
            self.wait_for_results()
            for idx, res in enumerate(self.proc_results):
                if 'sig_skipped' in res:
                    self.completed['__substep_skipped__'] += 1
                    self.completed['__substep_completed__'] -= 1
                if 'output' in res and env.sos_dict['step_output'].undetermined():
                    self.output_groups[idx] = res['output']
            # check results
            for proc_result in [x for x in self.proc_results if x['ret_code'] == 0]:
                if 'stdout' in proc_result and proc_result['stdout']:
                    sys.stdout.write(proc_result['stdout'])
                if 'stderr' in proc_result and proc_result['stderr']:
                    sys.stderr.write(proc_result['stderr'])

            for proc_result in [x for x in self.proc_results if x['ret_code'] != 0]:
                if 'stdout' in proc_result and proc_result['stdout']:
                    sys.stdout.write(proc_result['stdout'])
                if 'stderr' in proc_result and proc_result['stderr']:
                    sys.stderr.write(proc_result['stderr'])
                if 'exception' in proc_result:
                    raise proc_result['exception']
            # if output is Undetermined, re-evalulate it
            # finalize output from output_groups because some output might be skipped
            # this is the final version of the output but we do maintain output
            # during the execution of step, for compatibility.
            env.sos_dict.set(
                'step_output', sos_targets(self.output_groups[0]))
            for og in self.output_groups[1:]:
                env.sos_dict['step_output'].extend(og)
            env.sos_dict['step_output'].dedup()

            # now that output is settled, we can write remaining signatures
            for idx, res in enumerate(self.proc_results):
                if pending_signatures[idx] is not None:
                    if res['ret_code'] == 0:
                        pending_signatures[idx].write()

            # if there exists an option shared, the variable would be treated as
            # provides=sos_variable(), and then as step_output
            if 'shared' in self.step.options:
                self.shared_vars = evaluate_shared(self.shared_vars, self.step.options['shared'])
                env.sos_dict.quick_update(self.shared_vars)
            self.log('output')
            self.verify_output()
            substeps = self.completed['__substep_completed__'] + \
                self.completed['__substep_skipped__']
            self.completed['__step_completed__'] = self.completed['__substep_completed__'] / substeps
            self.completed['__step_skipped__'] = self.completed['__substep_skipped__'] / substeps
            if self.completed['__step_completed__'].is_integer():
                self.completed['__step_completed__'] = int(
                    self.completed['__step_completed__'])
            if self.completed['__step_skipped__'].is_integer():
                self.completed['__step_skipped__'] = int(
                    self.completed['__step_skipped__'])

            def file_only(targets):
                if not isinstance(targets, sos_targets):
                    env.logger.warning(
                        f"Unexpected input or output target for reporting. Empty list returned: {targets}")
                    return []
                else:
                    return [(str(x), x.size()) for x in targets._targets if isinstance(x, file_target)]
            step_info = {
                'step_id': self.step.md5,
                'start_time': self.start_time,
                'stepname': self.step.step_name(True),
                'substeps': len(self._substeps),
                'input': file_only(env.sos_dict['step_input']),
                'output': file_only(env.sos_dict['step_output']),
                'completed': dict(self.completed),
                'end_time': time.time()
            }
            workflow_signatures.write(
                'step', env.sos_dict["workflow_id"], repr(step_info))
            return self.collect_result()
        except KeyboardInterrupt:
            # if the worker_pool is not properly shutdown (e.g. interrupted by KeyboardInterrupt #871)
            # we try to kill all subprocesses. Because it takes time to shutdown all processes, impatient
            # users might hit Ctrl-C again, interrupting the shutdown process again. In this case we
            # simply catch the KeyboardInterrupt exception and try again.
            #
            if self.concurrent_substep and self.worker_pool:
                if env.verbosity > 2:
                    env.logger.info(f'{os.getpid()} terminating worker pool')
                while self.worker_pool:
                    try:
                        self.worker_pool.terminate()
                        SlotManager().release(self.worker_pool._processes - 1)
                        self.worker_pool = None
                    except KeyboardInterrupt:
                        continue

def _expand_file_list(ignore_unknown: bool, *args) -> sos_targets:
    ifiles = []

    for arg in args:
        if arg is None:
            continue
        elif isinstance(arg, BaseTarget):
            ifiles.append(arg)
        elif isinstance(arg, (str, path)):
            ifiles.append(os.path.expanduser(arg))
        elif isinstance(arg, sos_targets):
            ifiles.extend(arg.targets())
        elif isinstance(arg, paths):
            ifiles.extend(arg.paths())
        elif isinstance(arg, Iterable):
            # in case arg is a Generator, check its type will exhaust it
            arg = list(arg)
            if not all(isinstance(x, (str, path, BaseTarget)) for x in arg):
                raise RuntimeError(f'Invalid target: {arg}')
            ifiles.extend(arg)
        else:
            raise RuntimeError(
                f'Unrecognized file: {arg} of type {type(arg).__name__}')

    if ignore_unknown and all(isinstance(x, str) and '*' not in x for x in ifiles):
        # we are exclusind a case with
        #    output: *.txt, group_by
        # here but that case is conceptually wrong anyway
        return sos_targets(ifiles)
    # expand files with wildcard characters and check if files exist
    tmp = []
    for ifile in ifiles:
        if isinstance(ifile, BaseTarget):
            if ignore_unknown or ifile.target_exists():
                tmp.append(ifile)
            else:
                raise UnknownTarget(ifile)
        elif file_target(ifile).target_exists('target'):
            tmp.append(ifile)
        elif file_target(ifile).target_exists('any'):
            env.logger.debug(
                f'``{ifile}`` exists in zapped form (actual target has been removed).')
            tmp.append(ifile)
        elif isinstance(ifile, sos_targets):
            raise ValueError("sos_targets should not appear here")
        else:
            expanded = sorted(glob.glob(os.path.expanduser(ifile)))
            # no matching file ... but this is not a problem at the
            # inspection stage.
            #
            # NOTE: if a DAG is given, the input file can be output from
            # a previous step..
            #
            if not expanded:
                if ignore_unknown:
                    tmp.append(ifile)
                else:
                    raise UnknownTarget(file_target(ifile))
            else:
                tmp.extend(expanded)
    return sos_targets(tmp)


class Step_Executor(Base_Step_Executor):
    '''Single process step executor'''

    def __init__(self, step, pipe, mode='run'):
        self.run_mode = mode
        env.config['run_mode'] = mode
        if hasattr(env, 'accessed_vars'):
            delattr(env, 'accessed_vars')
        super(Step_Executor, self).__init__(step)
        self.pipe = pipe
        # because step is executed in a separate SoS_Worker process, this
        # __pipe__ is available to all the actions that will be executed
        # in the step
        env.__pipe__ = pipe

    def submit_tasks(self, tasks):
        env.logger.debug(f'Send {tasks}')
        if 'queue' in env.sos_dict['_runtime'] and env.sos_dict['_runtime']['queue']:
            host = env.sos_dict['_runtime']['queue']
        else:
            # otherwise, use workflow default
            host = '__default__'
        self.pipe.send(f'tasks {host} {" ".join(tasks)}')

    def wait_for_tasks(self, tasks):
        if not tasks:
            return {}
        # wait till the executor responde
        results = {}
        while True:
            res = self.pipe.recv()
            if res is None:
                sys.exit(0)
            results.update(res)
            # all results have been obtained.
            if len(results) == len(tasks):
                break
        return results

    def run(self):
        try:
            res = Base_Step_Executor.run(self)
            if self.pipe is not None:
                env.logger.debug(
                    f'Step {self.step.step_name()} sends result {short_repr(res)}')
                self.pipe.send(res)
            else:
                return res
        except Exception as e:
            if env.verbosity > 2:
                sys.stderr.write(get_traceback())
            if self.pipe is not None:
                env.logger.debug(
                    f'Step {self.step.step_name()} sends exception {e}')
                self.pipe.send(e)
            else:
                raise e
