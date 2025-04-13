"""
Polaris and Theta experiments
"""
import datetime
import datetime
from CqSim.Cqsim_plus import Cqsim_plus
from tqdm.auto import tqdm
from utils import probabilistic_true, disable_print
import pandas as pd
import random
import multiprocessing
from trace_utils import read_swf_generator, num_jobs_swf
import time

# All results will the stored within this directory
master_exp_directory = f'../data/Results/exp_polaris_theta'


def exp_theta(tqdm_pos, tqdm_lock, seed):
    random.seed(seed)
    """
    Experiment Theta

    Simulates Theta 2023 jobs on Theta

    """
    exp_name = 'only_theta'
    trace_dir = '../preprocessing/output'
    trace_file = 'theta_23.swf'
    cqp = Cqsim_plus()
    cqp.set_exp_directory(f'{master_exp_directory}/{exp_name}')

    # Cluster Theta
    theta_proc = 4360
    theta = cqp.single_cqsim(
        trace_dir, 
        trace_file, 
        proc_count=theta_proc,
        parsed_trace=False,
        sim_tag='theta')

    # Get the real unix submit time of first job
    read_job_gen = read_swf_generator(f'{trace_dir}/{trace_file}')
    first_job_submit_time = (next(read_job_gen))['submit']

    # Get the total number of jobs
    num_jobs = num_jobs_swf(f'{trace_dir}/{trace_file}')

    # Configure the simulators
    for sim in [theta]:
        # Read all jobs
        cqp.set_max_lines(sim, num_jobs)

        # Set the real time sart time and virtual start times
        cqp.set_sim_times(sim, real_start_time=first_job_submit_time, virtual_start_time=0)

        # Disbale the debug module
        cqp.disable_debug_module(sim)

    # Generator to read jobs
    read_job_gen = read_swf_generator(f'{trace_dir}/{trace_file}')


    tqdm_text = exp_name
    with tqdm_lock:
        bar = tqdm(
            desc=tqdm_text,
            total=num_jobs,
            position=tqdm_pos,
            leave=False)

    for i in range(num_jobs):

        # Get information on the next job
        job_data = next(read_job_gen)

        # Simulate it
        with disable_print():
            cqp.line_step(sim, write_results=False)

        with tqdm_lock:
            bar.update(1)

    with tqdm_lock:
        bar.close()

    # Run all the simulations until complete.
    while not cqp.check_all_sim_ended([theta]):
        for sim_id in [theta]:
            with disable_print():
                cqp.line_step(sim_id, write_results=False)

    return {
        "theta" : cqp.get_job_results(theta),
    }


def exp_polaris(tqdm_pos, tqdm_lock, seed):
    random.seed(seed)
    """
    Experiment Polaris

    Simulates Polaris 2023 jobs on Polaris
    """
    exp_name = 'only_polaris'
    trace_dir = '../preprocessing/output'
    trace_file = 'polaris_23.swf'
    cqp = Cqsim_plus()
    cqp.set_exp_directory(f'{master_exp_directory}/{exp_name}')


    # Cluster Polaris
    polaris_proc = 552
    polaris = cqp.single_cqsim(
        trace_dir, 
        trace_file, 
        proc_count=polaris_proc,
        parsed_trace=False,
        sim_tag='polaris')


    # Get the real unix submit time of first job
    read_job_gen = read_swf_generator(f'{trace_dir}/{trace_file}')
    first_job_submit_time = (next(read_job_gen))['submit']

    # Get the total number of jobs
    num_jobs = num_jobs_swf(f'{trace_dir}/{trace_file}')

    # Configure the simulators
    for sim in [polaris]:
        # Read all jobs
        cqp.set_max_lines(sim, num_jobs)

        # Set the real time sart time and virtual start times
        cqp.set_sim_times(sim, real_start_time=first_job_submit_time, virtual_start_time=0)

        # Disbale the debug module
        cqp.disable_debug_module(sim)

    # Generator to read jobs
    read_job_gen = read_swf_generator(f'{trace_dir}/{trace_file}')


    tqdm_text = exp_name
    with tqdm_lock:
        bar = tqdm(
            desc=tqdm_text,
            total=num_jobs,
            position=tqdm_pos,
            leave=False)

    for i in range(num_jobs):

        # Get information on the next job
        job_data = next(read_job_gen)
          
        # Simulate it
        with disable_print():
            cqp.line_step(sim, write_results=False)

        with tqdm_lock:
            bar.update(1)

    with tqdm_lock:
        bar.close()

    # Run all the simulations until complete.
    while not cqp.check_all_sim_ended([polaris]):
        for sim_id in [polaris]:
            with disable_print():
                cqp.line_step(sim_id, write_results=False)

    return {
        "polaris" : cqp.get_job_results(polaris)
    }


def exp_polaris_theta_random(tqdm_pos, tqdm_lock, seed):
    random.seed(seed)
    """
    Theta and Polaris Metascheduled using random allocation
    """
    exp_name = 'random'
    trace_dir = '../preprocessing/output'
    trace_file = 'polaris_theta_23.swf'
    cqp = Cqsim_plus()
    cqp.set_exp_directory(f'{master_exp_directory}/{exp_name}')

    # Cluster 1 is Theta
    theta_proc = 4360
    theta = cqp.single_cqsim(
        trace_dir, 
        trace_file, 
        proc_count=theta_proc,
        parsed_trace=False,
        sim_tag='theta')
    

    # Cluster 2 is Polaris
    polaris_proc = 552
    polaris = cqp.single_cqsim(
        trace_dir, 
        trace_file, 
        proc_count=polaris_proc,
        parsed_trace=False,
        sim_tag='polaris')


    # Get the real unix submit time of first job
    read_job_gen = read_swf_generator(f'{trace_dir}/{trace_file}')
    first_job_submit_time = (next(read_job_gen))['submit']

    # Get the total number of jobs
    num_jobs = num_jobs_swf(f'{trace_dir}/{trace_file}')

    # Configure the simulators
    for sim in [polaris, theta]:
        # Read all jobs
        cqp.set_max_lines(sim, num_jobs)

        # Set the real time sart time and virtual start times
        cqp.set_sim_times(sim, real_start_time=first_job_submit_time, virtual_start_time=0)

        # Disbale the debug module
        cqp.disable_debug_module(sim)

    # Generator to read jobs
    read_job_gen = read_swf_generator(f'{trace_dir}/{trace_file}')


    tqdm_text = exp_name
    with tqdm_lock:
        bar = tqdm(
            desc=tqdm_text,
            total=num_jobs,
            position=tqdm_pos,
            leave=False)

    for i in range(num_jobs):

        # Get information on the next job
        job_data = next(read_job_gen)

        if job_data['is_gpu'] == 1:

            # GPU jobs can only go to polaris
            selected_sim = polaris
        else:

            eligilbe_clusters = []
            # Find the clusters eligibe
            if job_data['req_proc'] <= polaris_proc:
                eligilbe_clusters.append(polaris)

            if job_data['req_proc'] <= theta_proc:
                eligilbe_clusters.append(theta)


            if eligilbe_clusters == 2:

                if probabilistic_true(0.6):
                    selected_sim = polaris
                else:
                    selected_sim = theta

            else:
                selected_sim = eligilbe_clusters[0]

        # Add the job to the appropriate cluster and continue main simulation.
        for sim in [polaris, theta]:

            if sim == selected_sim:

                if sim == polaris:
                    # Adjust cluster speeds
                    if job_data['cluster_id'] == 0:
                        # Originally a polaris job
                        cqp.set_job_run_scale_factor(sim, 1.0)
                        cqp.set_job_walltime_scale_factor(sim, 1.0)
                    elif job_data['cluster_id'] == 1:
                        # Originally a theta job
                        cqp.set_job_run_scale_factor(sim, 0.25)
                        cqp.set_job_walltime_scale_factor(sim, 0.25)
                elif sim == theta:
                    # Adjust cluster speeds
                    if job_data['cluster_id'] == 0:
                        # Originally a polaris job
                        cqp.set_job_run_scale_factor(sim, 4.0)
                        cqp.set_job_walltime_scale_factor(sim, 4.0)
                    elif job_data['cluster_id'] == 1:
                        # Originally a theta job
                        cqp.set_job_run_scale_factor(sim, 1.0)
                        cqp.set_job_walltime_scale_factor(sim, 1.0)

                # Enable the next job in the mask
                cqp.enable_next_job(sim)

            else:
                cqp.disable_next_job(sim)

            
            # Simulate it
            with disable_print():
                cqp.line_step(sim, write_results=False)

        #Reset cluster speeds
        for sim in [polaris, theta]:
            cqp.set_job_run_scale_factor(sim, 1.0)
            cqp.set_job_walltime_scale_factor(sim, 1.0)

        with tqdm_lock:
            bar.update(1)

    with tqdm_lock:
        bar.close()

    # Run all the simulations until complete.
    while not cqp.check_all_sim_ended([polaris, theta]):
        for sim_id in [polaris, theta]:
            with disable_print():
                cqp.line_step(sim_id, write_results=False)

    return {
        "theta" : cqp.get_job_results(theta),
        "polaris" : cqp.get_job_results(polaris)
    }


def exp_polaris_theta_sgst(tqdm_pos, tqdm_lock, seed):
    random.seed(seed)
    """
    Theta and Polaris Metascheduled using sgst
    """
    exp_name = 'sgst'
    trace_dir = '../preprocessing/output'
    trace_file = 'polaris_theta_23.swf'
    cqp = Cqsim_plus()
    cqp.set_exp_directory(f'{master_exp_directory}/{exp_name}')

    # Performance
    performance_column_names = ['job_id', 'mp_used', 'start', 'end']
    cqp.write_misc_data('performance.csv', ", ".join(performance_column_names) + '\n')

    # Define the simulators
    polaris_proc = 552
    polaris = cqp.single_cqsim(
        trace_dir, 
        trace_file, 
        proc_count=polaris_proc,
        parsed_trace=False,
        sim_tag='polaris')

    theta_proc = 4360
    theta = cqp.single_cqsim(
        trace_dir, 
        trace_file, 
        proc_count=theta_proc,
        parsed_trace=False,
        sim_tag='theta')

    # Get the real unix submit time of first job
    read_job_gen = read_swf_generator(f'{trace_dir}/{trace_file}')
    first_job_submit_time = (next(read_job_gen))['submit']

    # Get the total number of jobs
    num_jobs = num_jobs_swf(f'{trace_dir}/{trace_file}')

    # Configure the simulators
    for sim in [polaris, theta]:
        # Read all jobs
        cqp.set_max_lines(sim, num_jobs)

        # Set the real time sart time and virtual start times
        cqp.set_sim_times(sim, real_start_time=first_job_submit_time, virtual_start_time=0)

        # Disbale the debug module
        cqp.disable_debug_module(sim)

    # Generator to read jobs
    read_job_gen = read_swf_generator(f'{trace_dir}/{trace_file}')

    tqdm_text = exp_name
    with tqdm_lock:
        bar = tqdm(
            desc=tqdm_text,
            total=num_jobs,
            position=tqdm_pos,
            leave=False)

    for i in range(num_jobs):

        # Get information on the next job
        job_data = next(read_job_gen)

        cqp.write_misc_data('jobs.csv', f'job {job_data['id']}\n')
        
        if job_data['cluster_id'] == 0:
            cqp.write_misc_data('jobs.csv', f'polaris job\n')
        elif job_data['cluster_id'] == 1:
            cqp.write_misc_data('jobs.csv', f'theta job\n')


        t_start = time.time()
        mp_used = -1
        if job_data['is_gpu'] == 1:

            cqp.write_misc_data('jobs.csv', f'\tgpu job\n')

            mp_used = 0

            # GPU jobs can only go to polaris
            selected_sim = polaris

        else:
            mp_used = 1
            turnarounds = {}
            scale_factors = []

            # Adjust cluster speeds
            if job_data['cluster_id'] == 0:
                # Originally a polaris job
                scale_factors = [1.0, 4.0]

            elif job_data['cluster_id'] == 1:
                # Originally a theta job
                scale_factors = [0.25, 1.0]


            turnarounds = cqp.predict_next_job_turnarounds([polaris, theta], job_data['id'], job_data['req_proc'], scale_factors)

            cqp.write_misc_data('jobs.csv', f'\tturnarounds: {turnarounds}\n')

            # Sanity check
            assert(len(turnarounds) != 0)


            # Get the cluster with the lowest turnaround.
            lowest_turnaround = min(turnarounds.values())
            sims_with_lowest_turnaround = [key for key, value in turnarounds.items() if value == lowest_turnaround]

            # Ties are broken randomly
            selected_sim = random.choice(sims_with_lowest_turnaround)

            cqp.write_misc_data('jobs.csv', f'\tpredicted turnarounds: {turnarounds}\n')
        
        cqp.write_misc_data('jobs.csv', f'\tselected sim {'polaris' if selected_sim==polaris else 'theta'}\n')

        if job_data['cluster_id'] == 0:
            # Originally a polaris job
            cqp.set_job_run_scale_factor(polaris, 1.0)
            cqp.set_job_walltime_scale_factor(polaris, 1.0)
            cqp.set_job_run_scale_factor(theta, 4.0)
            cqp.set_job_walltime_scale_factor(theta, 4.0)
            cqp.write_misc_data('jobs.csv', f'\t\ttheta scaled by 4x\n')
        elif job_data['cluster_id'] == 1:
            # Originally a theta job
            cqp.set_job_run_scale_factor(polaris, 0.25)
            cqp.set_job_walltime_scale_factor(polaris, 0.25)
            cqp.set_job_run_scale_factor(theta, 1.0)
            cqp.set_job_walltime_scale_factor(theta, 1.0)
            cqp.write_misc_data('jobs.csv', f'\t\tpolaris scaled by 0.25x\n')
        else:
            assert True == False

        for sim in [polaris, theta]:

            if sim == selected_sim:
                # Enable the next job in the mask
                cqp.enable_next_job(sim)

            else:
                cqp.disable_next_job(sim)
            
            # Simulate it
            with disable_print():
                cqp.line_step(sim, write_results=False)


        t_end = time.time()

        job_performance_data = [str(e) for e in [job_data['id'],mp_used,t_start,t_end]]

        cqp.write_misc_data('performance.csv', ",".join(job_performance_data) + '\n')

        with tqdm_lock:
            bar.update(1)

    with tqdm_lock:
        bar.close()

    # Run all the simulations until complete.
    while not cqp.check_all_sim_ended([polaris, theta]):
        for sim_id in [polaris, theta]:
            with disable_print():
                cqp.line_step(sim_id, write_results=False)

    return {
        "theta" : cqp.get_job_results(theta),
        "polaris" : cqp.get_job_results(polaris)
    }



if __name__ == '__main__':

    # create_theta_cori_traces('../data/InputFiles', )

    lock = multiprocessing.Manager().Lock()
    p = []

    import sys
    selector = int(sys.argv[1])


    if selector == 0:
#        # Just theta
        p.append(multiprocessing.Process(target=exp_theta, args=(1, lock,)))

    if selector == 1:
        # Just Polaris
        p.append(multiprocessing.Process(target=exp_polaris, args=(1, lock,)))

    if selector == 2:
        # Theta Polaris opt turn
        p.append(multiprocessing.Process(target=exp_polaris_theta_sgst, args=(1, lock,)))

    if selector == 3:
        # Theta Polaris random
        p.append(multiprocessing.Process(target=exp_polaris_theta_random, args=(1, lock,)))
        pass

    if selector == 4:
        # Run all
        p.append(multiprocessing.Process(target=exp_theta, args=(1, lock,)))
        p.append(multiprocessing.Process(target=exp_polaris, args=(2, lock,)))
        p.append(multiprocessing.Process(target=exp_polaris_theta_sgst, args=(3, lock,)))
        p.append(multiprocessing.Process(target=exp_polaris_theta_random, args=(4, lock,)))


    for proc in p:
        proc.start()
    

    for proc in p:
        proc.join()