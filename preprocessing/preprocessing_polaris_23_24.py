"""
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
    'num_queue',      #15 Check if gpu is used or not
    'num_part',       #16
    'num_pre',        #17
    'think_time',     #18
    ]"""

import csv
from datetime import datetime
import os

# Function to convert timestamp to Unix time
def convert_to_unix(timestamp_str):
    """
    timestamp_str: "%Y-%m-%d %H:%M:%S" to unix timestamp
    """
    timestamp_format = "%Y-%m-%d %H:%M:%S"
    dt = datetime.strptime(timestamp_str, timestamp_format)
    return int(dt.timestamp())

# Function to read GPU job IDs from the GPU file
def read_gpu_jobs(gpu_jobs_file):
    gpu_job_ids = set()
    with open(gpu_jobs_file, 'r') as gpu_file:
        reader = csv.reader(gpu_file, delimiter=',')
        for row in reader:
            if row[7] == 'used':
                gpu_job_ids.add(row[5])
            else:
                continue
    return gpu_job_ids

# Function to convert the CSV file to the desired format
def anl_log_to_swf(in_anl_log_path, in_gpu_file_path, out_swf_path):
    gpu_job_ids = read_gpu_jobs(in_gpu_file_path)  # Store GPU job IDs in a set
    job_list = []
    
    with open(in_anl_log_path, 'r') as csv_file, open(out_swf_path, 'w') as output_file:
        reader = csv.DictReader(csv_file)
        id = 1
        for row in reader:
            # Extract the necessary fields from the CSV
            index = (row["JOB_NAME"]).split('.')[0]
            if '[' in index:
                index = index.split('[')[0]
            submit = convert_to_unix(row["QUEUED_TIMESTAMP"])
            start = convert_to_unix(row['START_TIMESTAMP'])
            wait = (convert_to_unix(row["START_TIMESTAMP"])) - (convert_to_unix(row["QUEUED_TIMESTAMP"]))
            runtime = (convert_to_unix(row["END_TIMESTAMP"])) - (convert_to_unix(row["START_TIMESTAMP"]))
            walltime = int(float(row["WALLTIME_SECONDS"]))
            used_proc = int(float(row["NODES_USED"]))
            req_proc = int(float(row["NODES_REQUESTED"]))
            type = (row["QUEUE_NAME"])
            cluster_id = 1
            if index in gpu_job_ids:
                num_queue = 1
            else:
                num_queue = 0

            # sep 1 2023 0:00:00 1693544400
            # sep 1 2024 0:00:00 1725166800
            
            if (type == 'debug' or type == 'debug-scaling') and req_proc <= 8:
                continue
            if (type == 'debug' or type == 'debug-scaling') and req_proc > 8:
                req_proc = req_proc - 8
                used_proc = used_proc - 8
            if submit > 1725166800 or start < 1693544400 or submit < 1693544400 or req_proc >= 552 or req_proc == 0 or used_proc == 0 or walltime == 0 or runtime < 0:
                continue
            else:
                temp_info = {
                    'index': id,
                    'submit': submit,
                    'wait': wait,
                    'walltime': walltime,
                    'runtime': runtime,
                    'usedProc': used_proc,
                    'reqProc': req_proc,
                    'type': type,
                    'cluster_id' : cluster_id,
                    'num_queue' : num_queue
                }

                # Append to the job list
                job_list.append(temp_info)
                id += 1
        
        # Sort jobs and assign new ids
        sorted_data = sorted(job_list, key=lambda x: x['submit'])
        for i, entry in enumerate(sorted_data):
            entry['index'] = i + 1
        job_list = sorted_data
            
        # Output to a file
        for job in job_list:
            output_file.write((str)(job['index']) + " " +
                                (str)(job['submit'])+ " " +
                                (str)(job['wait']) + " " +
                                (str)(job['runtime']) + " " +
                                (str)(job['usedProc']) + " " +
                                "-1" + " " +
                                "-1" + " " +
                                (str)(job['reqProc']) + " " +                             
                                (str)(job['walltime']) + " " +
                                "-1" + " " +
                                "0" + " " + 
                                (str)(job['cluster_id']) + " " + 
                                "-1" + " " +
                                "-1" + " " +
                                (str)(job['num_queue']) + " " +
                                "-1" + " " +
                                "-1" + " " +
                                "-1" + " " + "\n")

"""
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

"""


# Combining polaris
import pandas as pd

# Define column names for the SWF format
swf_columns = [
    'id', 'submit', 'wait', 'run', 'used_proc', 'used_ave_cpu',
    'used_mem', 'req_proc', 'req_time', 'req_mem', 'status',
    'cluster_id', 'cluster_job_id', 'num_exe', 'num_queue',
    'num_part', 'num_pre', 'think_time'
]

def load_swf_as_dataframe(filename, source):
    """Loads an SWF file into a Pandas DataFrame."""
    data = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith(";") or not line.strip():  # Skip comments and empty lines
                continue
            fields = line.strip().split()
            if len(fields) == 18:
                data.append([
                    int(fields[0]),    # job ID
                    int(fields[1]),    # submit time
                    int(fields[2]),    # wait time
                    int(fields[3]),    # run time
                    int(fields[4]),    # used processors
                    int(fields[5]),    # average CPU usage
                    int(fields[6]),    # used memory
                    int(fields[7]),    # requested processors
                    int(fields[8]),    # requested time
                    int(fields[9]),    # requested memory
                    int(fields[10]),   # status
                    source,            # cluster ID (mapped to Polaris or Theta)
                    -1,                # cluster job ID
                    int(fields[13]),   # num executed
                    int(fields[14]),   # gpu used
                    int(fields[15]),   # num partitioned
                    int(fields[16]),   # num preempted
                    int(fields[17])    # think time
                ])
    return pd.DataFrame(data, columns=swf_columns)

def combine_and_sort_swf_files(in_file1_path, in_file2_path, out_swf_path):
    """Combines and sorts two SWF files using Pandas DataFrames."""
    # Load both SWF files into dataframes
    polaris_23_df = load_swf_as_dataframe(in_file1_path, '-1')
    polaris_24_df = load_swf_as_dataframe(in_file2_path, '-1')

    # Concatenate the dataframes
    combined_df = pd.concat([polaris_23_df, polaris_24_df])

    # Sort by the 'submit' column
    combined_df = combined_df.sort_values(by='submit').reset_index(drop=True)

    # Assign new IDs (1-based indexing)
    combined_df['id'] = combined_df.index + 1

    # Write the combined and sorted dataframe to the output SWF file
    with open(out_swf_path, 'w') as output_file:
        output_file.write("; UnixStartTime: 0\n; MaxNodes: 552\n; MaxProcs: 552\n")
        for _, row in combined_df.iterrows():
            output_file.write(
                f"{row['id']} {row['submit']} {row['wait']} {row['run']} {row['used_proc']} "
                f"{row['used_ave_cpu']} {row['used_mem']} {row['req_proc']} {row['req_time']} "
                f"{row['req_mem']} {row['status']} {row['cluster_id']} {row['cluster_job_id']} "
                f"{row['num_exe']} {row['num_queue']} {row['num_part']} {row['num_pre']} {row['think_time']}\n"
            )

def unix_to_datetime(unix_timestamp):
    """
    Convert a Unix timestamp to MM-DD-YY HH:MM:SS format.
    
    Parameters:
        unix_timestamp (int): The Unix timestamp to convert.
        
    Returns:
        str: The formatted date and time as a string.
    """
    return datetime.fromtimestamp(unix_timestamp).strftime('%m-%d-%y %H:%M:%S')

def print_swf_file_statistics(in_swf_file_path):
    start_date_str = ""
    end_date_str = ""
    num_jobs = 0 
    num_gpu_jobs = 0
    num_non_gpu_jobs = 0
    wait = 0
    avg_wait = 0.0
    with open(in_swf_file_path, "r") as file:
        for line in file:
            if line.startswith(";") or not line.strip():  # Skip comments and empty lines
                continue
            fields = line.strip().split()
            if fields[0] == '1':
                start_date_str = unix_to_datetime(int(fields[1]))
            end_date_str = unix_to_datetime(int(fields[1]))
            num_jobs += 1
            if fields[14] == '1':
                num_gpu_jobs += 1
            else:
                num_non_gpu_jobs += 1
            wait += int(fields[2])

    avg_wait = wait/num_jobs

    #Printing the stats
    print(f'Start Date: {start_date_str}')
    print(f'End Date: {end_date_str}')
    print(f'Num jobs: {num_jobs}')
    print(f'Num gpu jobs: {num_gpu_jobs}')
    print(f'Num non gpu jobs: {num_non_gpu_jobs}')
    print(f'Original avg wait time: {avg_wait:.5f}')

if __name__ == "__main__":

    ###############################################
    # Input Directories and File Setup
    ###############################################

    # Setup input output directories
    input_dir = 'data'
    output_dir = 'output'

    if not os.path.exists(input_dir):
        os.makedirs(input_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Setup input file paths
    anl_polaris_23_path = os.path.join(input_dir, 'ANL-ALCF-DJC-POLARIS_20230101_20231231.csv')
    anl_polaris_24_path = os.path.join(input_dir, 'ANL-ALCF-DJC-POLARIS_20240101_20241031.csv')
    gpu_file_path = os.path.join(input_dir, 'job_summary_used_gpus.csv')

    # Setup output file paths
    polaris_23_swf_path = os.path.join(output_dir, 'polaris_23.swf')
    polaris_24_swf_path = os.path.join(output_dir, 'polaris_24.swf')
    polaris_23_24_swf_path = os.path.join(output_dir, 'polaris_23_24.swf')

    ###############################################
    # Polaris 2023 from September 1st
    ###############################################
    print('###############################################')
    print('Parsing Polaris 2023...')
    anl_log_to_swf(
        in_anl_log_path=anl_polaris_23_path,
        in_gpu_file_path= gpu_file_path,
        out_swf_path=polaris_23_swf_path)
    
    print_swf_file_statistics(polaris_23_swf_path)
    print('###############################################')

    ###############################################
    # Polaris 2024 till September 1st
    ###############################################
    print('###############################################')
    print('Parsing Polaris 2024...')
    anl_log_to_swf(
        in_anl_log_path=anl_polaris_24_path,
        in_gpu_file_path= gpu_file_path,
        out_swf_path=polaris_24_swf_path)
    
    print_swf_file_statistics(polaris_24_swf_path)
    print('###############################################')

    
    ###############################################
    # Polaris Sep 1 2023 to Sep 1 2024
    ###############################################
    print('###############################################')
    print('Creating Polaris 2023 + 2024...')
    combine_and_sort_swf_files(
        in_file1_path=polaris_23_swf_path,
        in_file2_path=polaris_24_swf_path,
        out_swf_path=polaris_23_24_swf_path)
    
    print_swf_file_statistics(polaris_23_24_swf_path)
    print('###############################################')