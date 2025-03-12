"""
This example shows a way to "step through" cqsim.
"""

from CqSim.Cqsim_plus import Cqsim_plus
from trace_utils import read_swf_generator, num_jobs_swf

exp_name = 'only_theta'
trace_dir = '../preprocessing/output'
trace_file = 'theta_23.swf'
cqp : Cqsim_plus = Cqsim_plus()
cqp.set_exp_directory(f'../data/Results/exp_debug/{exp_name}')

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

cqp.line_step(sim, write_results=False)
for i in range(1, num_jobs + 1):

    h = input('Press a key...')
    print('Reading job i:', i)
    # Get information on the next job
    job_data = next(read_job_gen)

    if (i % 2 == 0):
        cqp.set_job_run_scale_factor(theta, 2.0)
        cqp.set_job_walltime_scale_factor(theta, 2.0)


    # Simulate it
    cqp.line_step(sim, write_results=False)

    cqp.set_job_run_scale_factor(theta, 1.0)
    cqp.set_job_walltime_scale_factor(theta, 1.0)

    if i == 2:

        # should disable job 3
        cqp.disable_next_job(theta)
