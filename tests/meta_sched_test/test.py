import os
import sys
import pandas as pd
from contextlib import contextmanager
import multiprocessing

# NOTE: This function helps set up the cwd and also the correct
# imports for the version of cqsim being run
@contextmanager
def change_dir(new_dir):
    original_directory = os.getcwd()
    original_path = sys.path.copy()
    try:
        os.chdir(new_dir)
        sys.path.insert(0, os.getcwd())
        yield
    finally:
        os.chdir(original_directory)
        sys.path = original_path


def run_parallel(result_queue):
    # With the proper working directory and imports
    with change_dir('../../src'):
        lock = multiprocessing.Manager().Lock()
        from meta_sched_parallel import run_experiment
        result_meta_parallel = run_experiment(1.25, 1, lock)
        result_queue.put(result_meta_parallel)

def run_original(result_queue):
    # With the proper working directory and imports
    with change_dir('../../cqsim_original/src'):
        from meta_sched_test import run_experiment
        result_meta = run_experiment()
        result_queue.put(result_meta)


def get_result_as_df(result):
    column_names = ['id', 'proc1', 'proc2','walltime', 'run', 'wait', 'submit', 'start', 'end']
    split_data = [[float(val) for val in line.split(';')] for line in result]
    df = pd.DataFrame(split_data, columns=column_names)
    return df

# NOTE: Using multiprocessing so that there are no conflicting imports


return_queue = multiprocessing.Queue()
p = multiprocessing.Process(target=run_original, args=(return_queue,))
p.start()
result_meta = return_queue.get() 
p.join()

return_queue = multiprocessing.Queue()
p = multiprocessing.Process(target=run_parallel, args=(return_queue,))
p.start()
result_meta_parallel = return_queue.get()
p.join()


# Print the lenghts of the results for correctness reference
c1_result = get_result_as_df(result_meta['cluster 1'])
c1p_result = get_result_as_df(result_meta_parallel['cluster 1'])
c2_result = get_result_as_df(result_meta['cluster 2'])
c2p_result = get_result_as_df(result_meta_parallel['cluster 2'])

print()
if not c1_result['id'].equals(c1p_result['id']):
    print('[TEST FAILED] cluster 1 mismatch')
else:
    print('[TEST PASSED] cluster 1')

if not c2_result['id'].equals(c2p_result['id']):
    print('[TEST FAILED] cluster 2 mismatch')
else:
    print('[TEST PASSED] cluster 2')


# From here we have the plotting script.
import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=result_meta['test_data']['jobs_processed'], 
        y=result_meta['test_data']['time_elapsed'], 
        mode='lines+markers', 
        name='Original'))
fig.add_trace(
    go.Scatter(
        x=result_meta_parallel['test_data']['jobs_processed'], 
        y=result_meta_parallel['test_data']['time_elapsed'], 
        mode='lines+markers', 
        name='Using Child Processes'))

fig.update_layout(title='No. of jobs processed vs Time elapsed',
                  xaxis_title='No. of jobs processed',
                  yaxis_title='Time elapsed')

fig.write_image("jobs_vs_time.png")