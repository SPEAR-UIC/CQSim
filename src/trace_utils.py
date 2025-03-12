"""
Utility functions for trace file manipulations.
"""
import os
import sys
import csv
import IOModule.Debug_log as Class_Debug_log
import Extend.SWF.Filter_job_SWF as filter_job_ext
import Extend.SWF.Filter_node_SWF as filter_node_ext
import Extend.SWF.Node_struc_SWF as node_struc_ext
import pandas as pd
import shutil
import os
import utils

swf_columns = [
    'id',             #1
    'submit',         #2
    'wait',           #3
    'run',            #4
    'used_proc',      #5
    'used_ave_cpu',   #6
    'used_mem',       #7
    'req_proc',       #8
    'req_time',       #9
    'req_mem',        #10 
    'status',         #11
    'cluster_id',     #12 Changed from user_id to cluster_id
    'cluster_job_id', #13 Changed from group_id to cluster_job_id
    'num_exe',        #14
    'is_gpu',         #15 Changed from num_queue
    'num_part',       #16
    'num_pre',        #17
    'think_time',     #18
    ]


def num_jobs_swf(trace_path):
    counter = 0
    with open(trace_path, 'r') as swf_file:
        for line in swf_file:
            if line[0] == ';':
                continue
            else:
                counter+=1

    return counter

def read_swf_generator(trace_path):
    """
    Returns a generator object for reading swf files line by line.

    This avoids loading the entire job file into memory.
    """

    with open(trace_path, 'r') as swf_file:
        for line in swf_file:
            if line[0] == ';':
                continue
            
            row = [int(x) for x in line.split() if x]
            job_data = {k:v for k, v in zip(swf_columns, row)}
            yield job_data


def read_swf(trace_dir, trace_file):
    """
    Reads an SWF file into a dataframe

    Args:
        filename: The name of the file to read.

    Returns:
        A list of lists, where each inner list represents a processed line of input.
    """
    data = []

    with open(f'{trace_dir}/{trace_file}', 'r') as file:
        for line in file:
        
            # TODO: For now ignoring the header of the swf file
            if line[0] == ';':
                continue

            # Split the line into elements, convert non-empty elements to integers
            row = [int(x) for x in line.split() if x]
            data.append(row)
    df = pd.DataFrame(data, columns=swf_columns)
    return df


def read_job_data_swf(trace_dir, trace_file):
    """
    Read the job data from some trace.

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
    module_debug = Class_Debug_log.Debug_log(
        lvl=0,
        show=0,
        path= f'/dev/null',
        log_freq=1
    )
    module_debug.disable()
    save_name_j = f'trace.csv'
    config_name_j = f'/dev/null'
    module_filter_job = filter_job_ext.Filter_job_SWF(
        trace=f'{trace_dir}/{trace_file}', 
        save=save_name_j, 
        config=config_name_j, 
        debug=module_debug
    )
    module_filter_job.feed_job_trace()
    module_filter_job.output_job_config()

    df = pd.read_csv(f'trace.csv', sep=';', header=None) 
    utils.delete_file('trace.csv')
    df.columns = swf_columns
    return df
    
# trace_dir = '../data/InputFiles/theta_polaris_2023'
# trace_file = 'polaris_theta_2023.swf'
# df = read_swf(trace_dir, trace_file)
# print(df)