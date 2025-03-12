import os
import sys
import time
from multiprocessing import Process, Pipe
import json
from types import SimpleNamespace
import os


import IOModule.Log_print as Log_print
import CqSim.Cqsim_sim as Class_Cqsim_sim
import cqsim_path
import IOModule.Debug_log as Class_Debug_log
import IOModule.Output_log as Class_Output_log

import CqSim.Job_trace as Class_Job_trace
#import CqSim.Node_struc as Class_Node_struc
import CqSim.Backfill as Class_Backfill
import CqSim.Start_window as Class_Start_window
import CqSim.Basic_algorithm as Class_Basic_algorithm
import CqSim.Info_collect as Class_Info_collect
import CqSim.Cqsim_sim as Class_Cqsim_sim

import Extend.SWF.Filter_job_SWF as filter_job_ext
import Extend.SWF.Filter_node_SWF as filter_node_ext
import Extend.SWF.Node_struc_SWF as node_struc_ext
__metaclass__ = type
import pandas as pd
from CqSim.utils import swf_columns
from trace_utils import read_swf

class Cqsim_plus:
    """
    CQsim plus

    Class for CQSim plus core features.
    """


    def __init__(self, tag = None) -> None:
        """Initialize CQSim plus.

        Args:

        Attributes:
            monitor: interval for monitor event. (default: 500)
            sims: List of CQSim generator instances.
            line_counters: List of line counts in the job file for each cqsim instance.
            end_flags: List of end flags for each cqsim insance, denothing whether the simuation has ended.
            sim_names: List of names for each cqsim instance.
            sim_modules: List of CQSim modules for each cqsim instance.
            exp_directory: The directory for output files for all simulators.
            traces: A map from trace paths to simulator ids, prevents the parsing of a trace that was already parsed.
            disable_child_stdout: Flag to disable the stdout of the child. (default: False)
            tag: A string used to create output folder under ../data/Results/
        """
        
        self.monitor = 500
        self.sims = []
        self.line_counters=[]
        self.end_flags = []
        self.sim_names = []
        self.sim_modules = []
        self.sim_procs = []
        self.sim_uses_parsed_trace = []
        self.sim_tags = []
        # TODO: For now, each cqsim instance's IO folder is given a random name
        self.exp_directory = f'../data/Results/exp'
        self.disable_child_stdout = True
        self.tag = tag
        if self.tag != None:
            self.exp_directory = f'../data/Results/{self.tag}'

    def set_exp_directory(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
        self.exp_directory = dir

    def set_sim_times(self, id, real_start_time, virtual_start_time):
        job_module = self.sim_modules[id].module['job']
        job_module.real_start_time = real_start_time
        job_module.virtual_start_time = virtual_start_time


    def write_misc_data(self, file_name, data):

        if not os.path.exists(f'{self.exp_directory}/{file_name}'):
            with open(f'{self.exp_directory}/{file_name}', 'w') as f:
                pass

        with open(f'{self.exp_directory}/{file_name}', 'a') as f:
            f.write(data)
            

    def check_sim_ended(self, id):
        """
        Checks if the simulator with given id has ended.
        """
        return self.end_flags[id]


    def check_all_sim_ended(self, ids):
        """
        Checks if all the simulators with given ids have ended.

        Returns true, when all simulators have finished.
        """
        result = True
        for id in ids:
            result = result and self.end_flags[id]
        return result


    def get_job_data(self, trace_dir, trace_file, parsed_trace = False):
        """
        Get the job data from some trace.

        Parameters
        ----------
        trace_dir : str
            A path to the directory where the trace file is located.
        trace_file : str
            The trace file name to read.

        Returns
        -------
        job_ids : lits[int]
            List of job ids.
        job_procs : list[int]
            List of processes requested for each job.
        """
        if parsed_trace:
            df = pd.read_csv(f'{trace_dir}/{trace_file}', sep=';', header=None) 
            df.columns = swf_columns
            return df['id'].to_list(), df['req_proc'].to_list(), df['submit'].to_list()



        '''module_debug = Class_Debug_log.Debug_log(
            lvl=0,
            show=0,
            path= f'/dev/null',
            log_freq=1
        )
        module_debug.disable()
        save_name_j = f'/dev/null'
        config_name_j = f'/dev/null'
        module_filter_job = filter_job_ext.Filter_job_SWF(
            trace=f'{trace_dir}/{trace_file}', 
            save=save_name_j, 
            config=config_name_j, 
            debug=module_debug
        )
        count = module_filter_job.feed_job_trace()
        print(count)
        module_filter_job.output_job_config()'''

        swf_df = read_swf(trace_dir, trace_file)

        job_ids = swf_df['id'].tolist()
        job_procs = swf_df['req_proc'].tolist()
        job_submits = swf_df['submit'].tolist()

        return job_ids, job_procs, job_submits

        #job_ids = module_filter_job.job_ids
        #job_procs = module_filter_job.job_procs
        #job_submits = module_filter_job.job_submits

        #return job_ids, job_procs, job_submits
    
    def get_miscellaneous_data(self, trace_dir, trace_file, parsed_trace = False):
        """
        Get the miscellaneous job data from some trace.

        Parameters
        ----------
        trace_dir : str
            A path to the directory where the trace file is located.
        trace_file : str
            The trace file name to read.

        Returns
        -------
        job_ids : lits[int]
            List of job ids.
        job_procs : list[int]
            List of processes requested for each job.
        """
        if parsed_trace:
            df = pd.read_csv(f'{trace_dir}/{trace_file}', sep=';', header=None) 
            df.columns = swf_columns
            return df['id'].to_list(), df['req_proc'].to_list(), df['submit'].to_list()



        '''module_debug = Class_Debug_log.Debug_log(
            lvl=0,
            show=0,
            path= f'/dev/null',
            log_freq=1
        )
        module_debug.disable()
        save_name_j = f'/dev/null'
        config_name_j = f'/dev/null'
        module_filter_job = filter_job_ext.Filter_job_SWF(
            trace=f'{trace_dir}/{trace_file}', 
            save=save_name_j, 
            config=config_name_j, 
            debug=module_debug
        )
        module_filter_job.feed_job_trace()
        module_filter_job.output_job_config()'''

        swf_df = read_swf(trace_dir, trace_file)

        cluster_ids = swf_df['cluster_id'].tolist()
        gpu_req = swf_df['is_gpu'].tolist()

        return cluster_ids, gpu_req


    def single_cqsim(self, trace_dir, trace_file, proc_count, parsed_trace = False, sim_tag = 'sim'):
        """
        Sets up a single cqsim instance.

        Parameters
        ----------
        trace_dir : str
            A path to the directory where the trace file is located.
        trace_file : str
            The trace file name to read.
        proc_count: int
            The amount of processes for the simualted cluster.

        Returns
        -------
        sim_id : int
            An integer id of the newly created cqsim instance.
        """
        sim_id = len(self.sims)

        output_dir = f'{self.exp_directory}/{sim_tag}/Results'
        debug_dir = f'{self.exp_directory}/{sim_tag}/Debug'
        fmt_dir = f'{self.exp_directory}/{sim_tag}/Fmt'
        plus_dir = f'{self.exp_directory}/{sim_tag}/plus'

        for dir in [output_dir, debug_dir, fmt_dir, plus_dir]:
            if not os.path.exists(dir):
                os.makedirs(dir)

        trace_name = trace_file.split('.')[0]

        output_sys_file = f'{trace_name}.ult'
        output_adapt_file = f'{trace_name}.adp'
        output_result_file = f'{trace_name}.rst'

        # Debug module
        debug_log = f'{trace_name}_debug.log'
        module_debug = Class_Debug_log.Debug_log(
            lvl=3,
            show=2,
            path= f'{debug_dir}/{debug_log}',
            log_freq=1
        )
        self.module_debug = module_debug

        # Filter SWF module -- If needed
        fmt_job_file = f'{trace_name}.csv'
        fmt_job_config_file = f'{trace_name}.con'
        fmt_node_file = f'{trace_name}_node.csv'
        fmt_node_config_file = f'{trace_name}_node.con'
    
        # If the trace parsed is already in in .csv
        if parsed_trace:

            destination = f'{fmt_dir}/{fmt_job_file}'
            source = f'{trace_dir}/{trace_file}'

            from CqSim.utils import copy_file
            copy_file(source, destination)
            

            # Generate Node realted format files
            module_filter_node = filter_node_ext.Filter_node_SWF(
                struc=None,
                save=f'{fmt_dir}/{fmt_node_file}', 
                config=f'{fmt_dir}/{fmt_node_config_file}', 
                debug=module_debug
            )
            module_filter_node.static_node_struc(proc_count)
            module_filter_node.output_node_data()
            module_filter_node.output_node_config()
            pass

        # Parse SWF file
        else:
            module_filter_job = filter_job_ext.Filter_job_SWF(
                trace=f'{trace_dir}/{trace_file}', 
                save=f'{fmt_dir}/{fmt_job_file}', 
                config=f'{fmt_dir}/{fmt_job_config_file}', 
                debug=module_debug
            )
            module_filter_job.feed_job_trace()
            module_filter_job.output_job_config()

            module_filter_node = filter_node_ext.Filter_node_SWF(
                struc=f'{trace_dir}/{trace_file}',
                save=f'{fmt_dir}/{fmt_node_file}', 
                config=f'{fmt_dir}/{fmt_node_config_file}', 
                debug=module_debug
            )
            module_filter_node.static_node_struc(proc_count)
            module_filter_node.output_node_data()
            module_filter_node.output_node_config()




        # Job trace module
        module_job_trace = Class_Job_trace.Job_trace(
            job_file_path=f'{fmt_dir}/{fmt_job_file}',
            debug=module_debug,
            real_start_time=0,
            virtual_start_time=0,
            max_lines=1000
        )
        # module_job_trace.import_job_config(f'{fmt_dir}/{fmt_job_config_file}')

        # Node structure module
        module_node_struc = node_struc_ext.Node_struc_SWF(debug=module_debug)
        module_node_struc.import_node_file(f'{fmt_dir}/{fmt_node_file}')
        module_node_struc.import_node_config(f'{fmt_dir}/{fmt_node_config_file}')

        # Backfill module
        module_backfill = Class_Backfill.Backfill(
            mode=1,
            node_module=module_node_struc,
            debug=module_debug,
            para_list=None
        )

        # Start window module
        module_win = Class_Start_window.Start_window(
            mode=5,
            node_module=module_node_struc,
            debug=module_debug,
            para_list=['5', '0', '0'],
            para_list_ad=None)

        # Basic alg module
        module_alg = Class_Basic_algorithm.Basic_algorithm (
            element=[['w', '+', '2'],[1, 0, 1]],
            debug=module_debug,
            para_list=None
        )

        # Info collect module
        module_info_collect = Class_Info_collect.Info_collect (
            alg_module=module_alg,debug=module_debug)

        # Output module
        module_output_log = Class_Output_log.Output_log (
            output = {
                'sys':f'{output_dir}/{output_sys_file}', 
                'adapt':f'{output_dir}/{output_adapt_file}', 
                'result':f'{output_dir}/{output_result_file}'
            },
            log_freq=1
        )

        module_list = {
            'debug':module_debug,
            'job':module_job_trace,
            'node':module_node_struc,
            'backfill':module_backfill,
            'win':module_win,
            'alg':module_alg,
            'info':module_info_collect,
            'output':module_output_log
        }
    
        # CQSim module
        module_sim = Class_Cqsim_sim.Cqsim_sim(
            module=module_list, 
            debug=module_debug, 
            monitor = 500
        )

        # Get the generator object
        cqsim = module_sim.cqsim_sim()

        # If it works, dont touch :P
        next(cqsim)

        # Book keeping
        self.sims.append(cqsim)
        self.line_counters.append(0)
        self.end_flags.append(False)
        self.sim_modules.append(module_sim)
        self.sim_procs.append(proc_count)
        self.sim_uses_parsed_trace.append(parsed_trace)
        if sim_tag == 'sim':
            self.sim_tags.append(str(sim_id))
        else:
            self.sim_tags.append(sim_tag)
        return sim_id


    def rst_to_df(self, results):
        presults = [result.split(';') for result in results]
        df = pd.DataFrame(presults, columns = ['id', 'reqProc', 'reqProc2', 'walltime', 'run', 'wait', 'submit', 'start', 'end']) 
        df = df.astype(float)
        sorted_df = df.sort_values('submit')
        return sorted_df


    def predict_next_job_turnarounds(self, ids, job_id, job_proc, scale_factors):
        """
        Takes a list of simulators of given ids. Reads the next job.
        Runs the simulators in a child process and returns the turnarounds
        of the newly read job.

        Parameters
        ----------
        ids : list[int]
            id of a cqsim instances stored in self.sims

        Returns
        -------
        turnarounds : dict[sim_id -> float]
            a dict mapping sim_id to the turnarounds value for the given job_id

        """
        parent_conn, child_conn = Pipe()

        p = Process(target=self._predict_next_job_turnarounds, args=(ids, job_id, job_proc, scale_factors, child_conn,))
        p.start()
        child_conn.close()
        json_str = ""
        while True:
            try:
                msg = parent_conn.recv()
                json_str = json_str + msg
            except EOFError:  # Child closed the connection
                break
        p.join()
        parent_conn.close()

        results = json.loads(json_str)

        # Convert to the right data type
        # results return from json.loads hasa the keys as strings
        # the keys are the cluster ids which should be ints
        results = {int(k):float(v) for k,v in results.items()}

        return results
        
    
    def _predict_next_job_turnarounds(self, ids, job_id, job_proc, scale_factors, conn):

        turnarounds = {}
        for id, sf in zip(ids, scale_factors):


            if job_proc > self.sim_procs[id]:
                continue

            # Modify the job module so that no new jobs are read.
            job_module = self.sim_modules[id].module['job']
            job_module.update_max_lines(self.line_counters[id] + 1)
            job_module.job_runtime_scale_factor = sf
            job_module.job_walltime_scale_factor = sf

            # Set the scale factors

            # Disable outputs of debug, log and output modules.
            debug_module = self.sim_modules[id].module['debug']
            output_module = self.sim_modules[id].module['output']
            debug_module.disable()
            output_module.disable()

            if self.disable_child_stdout:
                with open(os.devnull, 'w') as sys.stdout:
                    while not self.check_sim_ended(id):
                        self.line_step(id)
            else:
                with open(f'runon_{self.line_counters[id]}.txt', 'w') as sys.stdout:
                    while not self.check_sim_ended(id):
                        self.line_step(id)

            df = output_module.get_result()
            # Get the results for the job we just simulated
            last_job_results = df.loc[df['id'] == job_id]

            # Get the turnaround of the latest job.
            last_job_turnaround = last_job_results['end'] - last_job_results['submit']
            turnarounds[id] = float(last_job_turnaround.iloc[0])
        
        json_string = json.dumps(turnarounds)
        conn.send(str(json_string))
        conn.close()




    def line_step(self, id, write_results = False) -> None:
        """
        Advances a certain simulator with given id by one line in the job file.

        Parameters
        ----------
        id : int
            id of a cqsim instance stored in self.sims
        write_results : Boolean
            write the results

        Returns
        -------
        None
        """
        try:
            next(self.sims[id])
            self.line_counters[id] += 1

            if write_results:
                results = self.run_on(id)
                dest_dir = f'{self.exp_directory}/plus/sim_{self.sim_tags[id]}'
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                df = self.rst_to_df(results)
                df.to_csv(f'{dest_dir}/result.csv', index=False)
                
        except StopIteration:
            self.end_flags[id] = True


    def run_on(self, id):
        """
        Creates a copy of the simulator with given id, and
        runs it to completion without new job input.

        Parameters
        ----------
        id : int
            id of a cqsim instance stored in self.sims

        Returns
        -------
        results: list[str]
           Job results of the copied simulator.

        """
        parent_conn, child_conn = Pipe()

        p = Process(target=self._run_on_child, args=(id, child_conn,))
        p.start()
        child_conn.close()
        results = []
        while True:
            try:
                msg = parent_conn.recv()
                results.append(msg)
            except EOFError:  # Child closed the connection
                break
        p.join()
        parent_conn.close()
        return results


    def _run_on_child(self, id, conn):
        """
        This function is a helper for run_on(). The function is run inside a 
        child process which contains the copy of a simulator. The copied
        simulator is run to completion without new job input.

        Parameters
        ----------
        id : int
            id of a cqsim instance stored in self.sims
        
        conn:
            piped connection for the child to send results back to parent process.

        Returns
        -------
        None
        """
        
        # Get the modules
        job_module = self.sim_modules[id].module['job']
        debug_module = self.sim_modules[id].module['debug']
        output_module = self.sim_modules[id].module['output']

        # Modify the job module so that no new jobs are read.
        job_module.update_max_lines(self.line_counters[id])

        # Disable outputs of debug, log and output modules.
        debug_module.disable()
        output_module.disable()

        if self.disable_child_stdout:
            with open(os.devnull, 'w') as sys.stdout:
                while not self.check_sim_ended(id):
                    self.line_step(id)
        else:
            with open(f'runon_{self.line_counters[id]}.txt', 'w') as sys.stdout:
                while not self.check_sim_ended(id):
                    self.line_step(id)
        output_module.send_result_to_pipe(conn)
        conn.close()


    def line_step_run_on(self, id):
        """
        Creates a copy of the simulator with given id. The copied
        simulator is advanced by one step in the job file then run
        to completion withtout any new jobs.

        Parameters
        ----------
        id : int
            id of a cqsim instance stored in self.sims

        Returns
        -------
        results: list[str]
           Job results of the copied simulator.
        """
        parent_conn, child_conn = Pipe()

        p = Process(target=self._line_step_run_on_child, args=(id, child_conn,))
        p.start()
        child_conn.close()
        results = []
        while True:
            try:
                msg = parent_conn.recv()
                results.append(msg)
            except EOFError:  # Child closed the connection
                break
        p.join()
        parent_conn.close()
        return results


    def line_step_run_on_fork_based(self, id):
        """
        Same as line_step_run_on(), but used tradiation fork() instead
        of multiprocessing.

        Parameters
        ----------
        id : int
            id of a cqsim instance stored in self.sims

        Returns
        -------
        results: list[str]
           Job results of the copied simulator.
        """
        parent_conn, child_conn = Pipe()
        pid = os.fork()

        if pid == 0:  # Child process
            parent_conn.close()  # Close the parent's end in the child
            self._line_step_run_on_child(id, child_conn)
            os._exit(0)  # Ensure clean exit from child

        else:  # Parent process
            child_conn.close()  # Close the child's end in the parent
            result_file_lines = []
            while True:
                try:
                    msg = parent_conn.recv()
                    result_file_lines.append(msg)
                except EOFError:
                    break

            _, status = os.waitpid(pid, 0)  # Wait for child to finish
            parent_conn.close()
            return result_file_lines


    def _line_step_run_on_child(self, id, conn):
        """
        This function is a helper for line_step_run_on(). The function is run 
        inside a child process which contains the copy of a simulator. The copied
        simulator is advanced by one job then run to completion without any new
        job input.

        Parameters
        ----------
        id : int
            id of a cqsim instance stored in self.sims
        
        conn:
            piped connection for the child to send results back to parent process.

        Returns
        -------
        None
        """

        # Modify the job module so that no new jobs are read.
        job_module = self.sim_modules[id].module['job']
        job_module.update_max_lines(self.line_counters[id] + 1)

        # Disable outputs of debug, log and output modules.
        debug_module = self.sim_modules[id].module['debug']
        output_module = self.sim_modules[id].module['output']
        debug_module.disable()
        output_module.disable()

        if self.disable_child_stdout:
            with open(os.devnull, 'w') as sys.stdout:
                while not self.check_sim_ended(id):
                    self.line_step(id)
        else:
            with open(f'runon_{self.line_counters[id]}.txt', 'w') as sys.stdout:
                while not self.check_sim_ended(id):
                    self.line_step(id)
        output_module.send_result_to_pipe(conn)
        conn.close()


    def set_max_lines(self, id, max_lines):
        """
        For a certain simulator, set the max_lines parameter in the 
        job module. The max_line parameters controls the maximum
        number of lines to read from the job file.

        Parameters
        ----------
        id : int
            id of a cqsim instance stored in self.sims.
        
        max_lines: int
            Maximum number of lines to read from the job file.

        Returns
        -------
        None
        """
        job_module = self.sim_modules[id].module['job']
        job_module.update_max_lines(max_lines)


    def set_job_run_scale_factor(self, id, scale_factor):
        """
        For a certain simulator, this sets the factor by which the job runtime
        should be scaled.

        Parameters
        ----------
        id : int
            id of a cqsim instance stored in self.sims
        
        scale_factor: float
            The factor the scale the job runtimes by

        Returns
        -------
        None
        """
        job_module = self.sim_modules[id].module['job']
        job_module.job_runtime_scale_factor = scale_factor


    def set_job_walltime_scale_factor(self, id, scale_factor):
        """
        For a certain simulator, this sets the factor by which the job walltime
        should be scaled.

        Parameters
        ----------
        id : int
            id of a cqsim instance stored in self.sims
        
        scale_factor: float
            The factor the scale the job runtimes by

        Returns
        -------
        None
        """
        job_module = self.sim_modules[id].module['job']
        job_module.job_walltime_scale_factor = scale_factor
    
    def disable_next_job(self, id):
        """
        For a certain simulator, this sets the mask to 0 for the next
        job.

        Parameters
        ----------
        id : int
            id of a cqsim instance stored in self.sims

        Returns
        -------
        """
        job_module = self.sim_modules[id].module['job']
        job_module.disable_job(self.line_counters[id])

    
    def enable_next_job(self, id):
        """
        For a certain simulator, this sets the mask to 1 for the next
        job.

        Parameters
        ----------
        id : int
            id of a cqsim instance stored in self.sims

        Returns
        -------
        """
        job_module = self.sim_modules[id].module['job']
        job_module.enable_job(self.line_counters[id])
    
    def get_job_file_mask(self, id):
        """
        Get the job file mask for some simulator.

        Parameters
        ----------
        id : int
            id of a cqsim instance stored in self.sims.

        Returns
        -------
        mask: list[int]
            A list of 0s and 1s per line in the job file.
        """
        mask: list[int] = self.sim_modules[id].module['job'].mask
        return mask
    
    def set_job_file_mask(self, id, mask):
        """
        For a certain simulator, this sets the mask to 1 for the next.
        job.

        Parameters
        ----------
        id : int
            id of a cqsim instance stored in self.sims.

        mask: list[int]
            A list of 0s and 1s per line in the job file.

        Returns
        -------
        """
        self.sim_modules[id].module['job'].mask = mask

    
    def get_job_results(self, id):
        """
        For a certain simulator, get job relted results.

        Parameters
        ----------
        id : int
            id of a cqsim instance stored in self.sims.

        Returns
        -------
        results: list[str]
           For a certain simulator, this returns the results from 
           the output module. The same can be found in the .rst file.

        """
        output_module = self.sim_modules[id].module['output']
        results: list[str] = output_module.results
        return results
    
    def get_job_submits(self, trace_dir, trace_file):
        module_debug = Class_Debug_log.Debug_log(
            lvl=0,
            show=0,
            path= f'/dev/null',
            log_freq=1
        )
        module_debug.disable()
        save_name_j = f'/dev/null'
        config_name_j = f'/dev/null'
        module_filter_job = filter_job_ext.Filter_job_SWF(
            trace=f'{trace_dir}/{trace_file}', 
            save=save_name_j, 
            config=config_name_j, 
            debug=module_debug
        )
        module_filter_job.feed_job_trace()
        module_filter_job.output_job_config()

        job_submits = module_filter_job.job_submits
        return job_submits
    

    def print_results(self, id):
        output_module = self.sim_modules[id].module['output']
        output_module.print_saved_results()

    def disable_debug_module(self, id):
        """
        Disable the printing from the debug module.
        
        Parameters
        ----------
        id : int
            id of a cqsim instance stored in self.sims.

        Returns
        -------
        None
        """
        debug_module = self.sim_modules[id].module['debug']
        debug_module.disable()