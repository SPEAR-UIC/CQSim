# CQSim+ API

CQSim is built on python modules where each must be imported individually to construct any sort of experimental setup. CQSim+ offers a single class wrapper called Cqsim_plus defined in src/CqSim/Cqsim_plus.py. This class imports all required modules and implements logic for creating multiple simulation instances as well as prediction using multi-processing. A simple program written using the API of Cqsim_plus is documented below:

The following example shows how to simulate a single instance of a cluster
```
# Import cqsim plus
from CqSim.Cqsim_plus import Cqsim_plus

exp_name = 'only_theta'
trace_dir = '../preprocessing/output'
trace_file = 'theta_23.swf'
output_dir = f'../data/Results/exp_polaris_theta/{exp_name}'

# Create cqsim plus class
cqp = Cqsim_plus()
cqp.set_exp_directory(output_dir)


# Create a simulation instance
theta = cqp.single_cqsim(
    trace_dir, 
    trace_file, 
    proc_count=4360,
    parsed_trace=False,
    sim_tag='theta')

# Get the real unix submit time of first job
read_job_gen = read_swf_generator(f'{trace_dir}/{trace_file}')
first_job_submit_time = (next(read_job_gen))['submit']

# Get the total number of jobs (function provided in trace_utils.py)
num_jobs = num_jobs_swf(f'{trace_dir}/{trace_file}')

# Configure to read all the jobs
cqp.set_max_lines(theta, num_jobs)

# Set the real time sart time and virtual start times
cqp.set_sim_times(theta, real_start_time=first_job_submit_time, virtual_start_time=0)

# Disbale the debug module
cqp.disable_debug_module(theta)

# Generator to read jobs (function provided in trace_utils.py)
read_job_gen = read_swf_generator(f'{trace_dir}/{trace_file}')

 for i in range(num_jobs):

    # Simulate it
    # The line step function reads exactly one job from the trace file for simulation
    cqp.line_step(sim, write_results=False)

# After all jobs are read from the job file, continue simulation till the end
while not cqp.check_sim_ended(theta):
    cqp.line_step(theta, write_results=False)

```

For examples that simulate multiple clusters and use multi-process prediction see files src/exp_theta_two_parts.py and src/exp_polaris_theta.py. The first one corresponds to the experiments in the paper cited above and the second one is the case study from the same paper.


Once a python file with the experimental setup is created, simply running the file with the experiment should also run the simualtor.
