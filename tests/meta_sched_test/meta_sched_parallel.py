# import sys
# sys.path.insert(0, '../../src')
import tqdm
import time
import pandas as pd
import random
import builtins
import contextlib
from CqSim.Cqsim_plus import Cqsim_plus

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

def run_experiment(x, tqdm_pos, tqdm_lock):
    """
    Experiment 2

    Cluster setup:
        Cluster 1 uses original runtime
        Cluster 2 runs at a factor of x

    Scheduling Strategy:
        Always select the cluster with the lowest turnaround.
    """

    random.seed(100)
    test_data = {
        'time_elapsed' : [],
        'jobs_processed' : []
    }

    tag = f'theta_100_test'
    trace_dir = '../data/InputFiles'
    trace_file = 'theta_100.swf'
    cluster1_proc = 2180
    cluster2_proc = 2180


    cqp = Cqsim_plus(tag = tag)
    cqp.disable_child_stdout = True

    # Cluster 1 original runtime.
    id1 = cqp.single_cqsim(
        trace_dir, 
        trace_file, 
        proc_count=cluster1_proc)
    

    # Cluster 2 runs at a factor of x.
    id2 = cqp.single_cqsim(
        trace_dir, 
        trace_file, 
        proc_count=cluster2_proc)
    cqp.set_job_run_scale_factor(id2, x)
    cqp.set_job_walltime_scale_factor(id2, x)

    sims = [id1, id2]


    # Get job stats
    job_ids, job_procs = cqp.get_job_data(trace_dir, trace_file)
    job_submits = cqp.get_job_submits(trace_dir, trace_file)

    # Configure sims to read all jobs
    for sim in sims:
        cqp.set_max_lines(sim, len(job_ids))
        cqp.set_sim_times(sim, real_start_time=job_submits[0], virtual_start_time=0)

    tqdm_text = tag
    with tqdm_lock:
        bar = tqdm.tqdm(
            desc=tqdm_text,
            total=len(job_ids),
            position=tqdm_pos,
            leave=False)
    start_time = time.time()
    for i in range(len(job_ids)):


        turnarounds = {}
        # First simulate the new job on both clusters.
        for sim in sims:

            # Check if the job can be run.
            if job_procs[i] > cqp.sim_procs[sim]:
                continue
            
            # Run the simulation for only upto the next job.
            results = cqp.line_step_run_on(sim)

            # Parse the results
            presults = [result.split(';') for result in results]
            df = pd.DataFrame(presults, columns = ['id', 'reqProc', 'reqProc2', 'walltime', 'run', 'wait', 'submit', 'start', 'end']) 
            df = df.astype(float)
            index_of_max_value = df['id'].idxmax()
            last_job_results = df.loc[index_of_max_value]

            # Get the turnaround of the latest job.
            last_job_turnaround = last_job_results['end'] - last_job_results['submit']
            turnarounds[sim] = last_job_turnaround.item()

        # If none of the clusters could run, skip the job.
        if len(turnarounds) == 0:
            for sim in sims:
                cqp.disable_next_job(sim)
                with disable_print():
                    cqp.line_step(sim)
            continue
        

        # Get the cluster with the lowest turnaround.
        lowest_turnaround = min(turnarounds.values())
        sims_with_lowest_turnaround = [key for key, value in turnarounds.items() if value == lowest_turnaround]
        selected_sim = random.choice(sims_with_lowest_turnaround)

        # Add the job to the appropriate cluster and continue main simulation.
        for sim in sims:
            if sim == selected_sim:
                cqp.enable_next_job(sim)            
            else:
                cqp.disable_next_job(sim)
            with disable_print():
                cqp.line_step(sim)
        

        bar.update(1)

        time_elapsed = time.time() - start_time
        test_data['time_elapsed'].append(time_elapsed)
        test_data['jobs_processed'].append(i+1)

    
    bar.close()

    # Run all the simulations until complete.
    while not cqp.check_all_sim_ended(sims):
        for sim_id in sims:
            with disable_print():
                cqp.line_step(sim_id)

    result = {
        "cluster 1" : cqp.get_job_results(sims[0]),
        "cluster 2" : cqp.get_job_results(sims[1]),
        "test_data" : test_data
    }
    return result
