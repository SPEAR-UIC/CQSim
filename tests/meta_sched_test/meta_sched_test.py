import os
import random
from tqdm import trange
import time
# import cqsim_path
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


debug = f'../data/Debug'
results = f'../data/Results'
fmt = f'../data/Fmt'
paths = [debug, results, fmt]
for path in paths:
    if not os.path.exists(path):
        os.makedirs(path)


trace_dir = "../data/InputFiles/"
trace_name = 'theta_100'
clusters = [2180, 2180]
cluster_speeds = [1, 1.25]

# trace_name = 'test'
# clusters = [100, 120]
# cluster_speeds = [1.5, 1]

import builtins
import contextlib

@contextlib.contextmanager
def disable_print():
  """Temporarily disables the print function."""
  original_print = builtins.print

  def disabled_print(*args, **kwargs):
    pass  # Do nothing when print is called

  builtins.print = disabled_print
  try:
    yield
  finally:
    builtins.print = original_print

@contextlib.contextmanager
def enable_print():
  """Context manager that ensures printing is enabled, even if previously disabled."""
  original_print = builtins.print
  builtins.print = original_print  # Restore original print if needed
  try:
    yield
  finally:
    pass  # No need to do anything in the finally block

def read_swf(filename):
  """
  Reads the input from the specified file and processes each line into a list of integers.

  Args:
    filename: The name of the file to read.

  Returns:
    A list of lists, where each inner list represents a processed line of input.
  """
  data = []

  with open(filename, 'r') as file:
    for line in file:
      
      # TODO: For now ignoring the header of the swf file
      if line[0] == ';':
        continue
      data.append(line)

  return data

def get_job_data():

    module_debug = Class_Debug_log.Debug_log(
        lvl=0,
        show=0,
        path= f'../data/Debug/debug_{trace_name}.log',
        log_freq=1
    )
    save_name_j = f'../data/Fmt/{trace_name}.csv'
    config_name_j = f'../data/Fmt/{trace_name}.con'
    module_filter_job = filter_job_ext.Filter_job_SWF(
        trace=f'{trace_dir}{trace_name}.swf', 
        save=save_name_j, 
        config=config_name_j, 
        debug=module_debug
    )
    module_filter_job.feed_job_trace()
    module_filter_job.output_job_config()
    return module_filter_job.jobNum, module_filter_job.job_ids, module_filter_job.job_procs, module_filter_job.job_submits

def run_simulation(
      trace_name, trace_dir, mask, mask_max_i, proc_count, speed, start_time,
      output_sys = "../data/Results/" + trace_name + ".ult",
        output_adapt = "../data/Results/" + trace_name + ".adp",
        output_result = "../data/Results/" + trace_name + ".rst",
      ):

    with disable_print():
        print(".................... Debug")
        module_debug = Class_Debug_log.Debug_log(
            lvl=3,
            show=2,
            path= f'../data/Debug/debug_{trace_name}.log',
            log_freq=1
        )

        print(".................... Job Filter")
        save_name_j = f'../data/Fmt/{trace_name}.csv'
        config_name_j = f'../data/Fmt/{trace_name}.con'
        module_filter_job = filter_job_ext.Filter_job_SWF(
            trace=f'{trace_dir}{trace_name}.swf', 
            save=save_name_j, 
            config=config_name_j, 
            debug=module_debug
        )
        module_filter_job.feed_job_trace_with_mask_speed(mask, mask_max_i,speed)
        module_filter_job.output_job_config()


        print(".................... Node Filter")
        save_name_n = f'../data/Fmt/{trace_name}_node.csv'
        config_name_n = f'../data/Fmt/{trace_name}_node.con'
        module_filter_node = filter_node_ext.Filter_node_SWF(
            struc=f'{trace_dir}{trace_name}.swf',
            save=save_name_n, 
            config=config_name_n, 
            debug=module_debug
        )
        module_filter_node.static_node_struc(proc_count)
        module_filter_node.output_node_data()
        module_filter_node.output_node_config()

        print(".................... Job Trace")
        module_job_trace = Class_Job_trace.Job_trace(
            start=start_time,
            num=8000,
            anchor=0,
            density=1,
            read_input_freq=1000,
            debug=module_debug
        )
        module_job_trace.initial_import_job_file(save_name_j)
        module_job_trace.import_job_config(config_name_j)

        print(".................... Node Structure")
        module_node_struc = node_struc_ext.Node_struc_SWF(debug=module_debug)
        module_node_struc.import_node_file(save_name_n)
        module_node_struc.import_node_config(config_name_n)

        print(".................... Backfill")
        module_backfill = Class_Backfill.Backfill(
            mode=2,
            node_module=module_node_struc,
            debug=module_debug,
            para_list=None
        )


        print(".................... Start Window")
        module_win = Class_Start_window.Start_window(
            mode=5,
            node_module=module_node_struc,
            debug=module_debug,
            para_list=['5', '0', '0'],
            para_list_ad=None)


        print(".................... Basic Algorithm")
        module_alg = Class_Basic_algorithm.Basic_algorithm (
            element=[['w', '+', '2'],[1, 0, 1]],
            debug=module_debug,
            para_list=None
        )


        print(".................... Information Collect")
        module_info_collect = Class_Info_collect.Info_collect (
            alg_module=module_alg,debug=module_debug)

        print(".................... Output Log")
        module_output_log = Class_Output_log.Output_log (
            output = {
                'sys':output_sys, 
                'adapt':output_adapt, 
                'result':output_result
            },
            log_freq=1
        )

        print(".................... Cqsim Simulator")
        module_list = {
            'job':module_job_trace,
            'node':module_node_struc,
            'backfill':module_backfill,
            'win':module_win,
            'alg':module_alg,
            'info':module_info_collect,
            'output':module_output_log
        }
        module_sim = Class_Cqsim_sim.Cqsim_sim(
            module=module_list, 
            debug=module_debug, 
            monitor = 500
        )
        module_sim.cqsim_sim()
        return module_output_log.job_turnarounds, module_output_log.results
    
def run_experiment():
    random.seed(100)

    test_data = {
        'time_elapsed' : [],
        'jobs_processed' : []
    }

    job_count, job_ids, job_procs, job_submits = get_job_data()

    cluster_masks = [[0 for _ in range(job_count)] for c in clusters]
    export_data = []
    # job_count = 1000
    # Read jobs one by one
    start_time = time.time()
    for i in trange(job_count):

        # Simulate the clusters and find the turnarounds
        cluster_latest_job_turnarounds = {}
        for j in range(len(clusters)):

            # Check if the cluster can run the job
            if job_procs[i] > clusters[j]:
                continue

            # Add the job to the cluster for simualtion
            cluster_masks[j][i] = 1

            # Run the simulation
            turnarounds, _ = run_simulation(
                trace_name,
                trace_dir, 
                cluster_masks[j], # Mask for the jobs that should be considered
                i, # Max number of jobs to simulate
                clusters[j], # proc count for the cluster
                cluster_speeds[j], # speed of the cluster
                job_submits[0]
            )

            # Remove the job after simulation
            cluster_masks[j][i] = 0

            # Find the turnaround of the last job
            latest_job_turnaround = turnarounds[job_ids[i]]["turnaround"]
            cluster_latest_job_turnarounds[j] = latest_job_turnaround
        
        # If no clusters can run, skip the job
        if len(cluster_latest_job_turnarounds.values()) == 0:
            continue
        
        # Find the cluster with the lowest turnaround
        lowest_turnaround = min(cluster_latest_job_turnarounds.values())
        cluster_index_with_lowest_turnaround = [key for key, value in cluster_latest_job_turnarounds.items() if value == lowest_turnaround]

        selected_cluster_i = random.choice(cluster_index_with_lowest_turnaround)

        # Add the job
        cluster_masks[selected_cluster_i][i] = 1

        # Gernete output
        line = ''
        line += f'{job_ids[i]};{job_procs[i]};'
        for j in range(len(clusters)):
            if j in cluster_latest_job_turnarounds:
                line += f'{clusters[j]};{cluster_latest_job_turnarounds[j]};'
            else:
                line += f'{clusters[j]};-1;'
        line += f'{clusters[selected_cluster_i]}\n'
        export_data.append(line)
        #print(line, end='')
        ## Pretty Print
        # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # print(f'Job Id: {job_ids[i]}\tProc: {job_procs[i]}')
        # for j in range(len(clusters)):
        #     if j in cluster_latest_job_turnarounds:
        #         print(f'\tCluster: {clusters[j]}\tTurnaround: {cluster_latest_job_turnarounds[j]}')
        #     else:
        #        print(f'\tCluster: {clusters[j]}\tTurnaround: {-1}')
        # print(f'Selected cluster: {clusters[selected_cluster_i]}')
        # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

        time_elapsed = time.time() - start_time
        test_data['time_elapsed'].append(time_elapsed)
        test_data['jobs_processed'].append(i+1)

    result_file_names = []
    result_dir = f'../data/Results/{trace_name}/'
    if not os.path.exists(result_dir):
            os.makedirs(result_dir)

    # ### Generate the SWF separated files
    file_descriptors = []
    for j in range(len(clusters)):
        file_name = f'cluster_{j}_{clusters[j]}_{cluster_speeds[j]*100}.swf'
        file_path = result_dir + file_name
        result_file_names.append(file_name)
        f = open(file_path, 'w+')
        f.write(f'; UnixStartTime: 0\n')
        f.write(f'; MaxNodes: {clusters[j]}\n')
        f.write(f'; MaxProcs: {clusters[j]}\n')
        file_descriptors.append(f)

    o_swf = read_swf(f'{trace_dir}{trace_name}.swf')

    for i in range(job_count):
        # Find the cluster the job was assigned to
        assigned_cluster_i = -1
        for j in range(len(clusters)):
            if cluster_masks[j][i] == 1:
                assigned_cluster_i = j
                break
        if assigned_cluster_i == -1:
            continue
        f = file_descriptors[assigned_cluster_i]
        # print(o_swf[i])
        f.write(o_swf[i])

    for f in file_descriptors:
        f.close()
            

    ### Re-run simulation on final files to produce result files
    results = []
    for j in range(len(clusters)):
        print(f'Final simulation of {j}, {clusters[j]}, {cluster_speeds[j]}')
        _, result = run_simulation(
                trace_name,
                trace_dir,
                cluster_masks[j],
                len(cluster_masks[j]),
                clusters[j],
                cluster_speeds[j],
                job_submits[0],
                output_sys = "../data/Results/" + trace_name + '/' + result_file_names[j].split('.')[0] + ".ult",
                output_adapt = "../data/Results/" + trace_name + '/' + result_file_names[j].split('.')[0] + ".adp",
                output_result = "../data/Results/" + trace_name + '/' + result_file_names[j].split('.')[0] + ".rst",
        )
        results.append(result)
    result = {
       "cluster 1" : results[0],
       "cluster 2" : results[1],
       "test_data" : test_data
    }
    
    return result