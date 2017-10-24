# CQSim - A Trace-based Event-Driven Scheduling Simulator
This version was originally developed by Xingwu Zheng SPEAR group of Illinois Institute of Technology. 

The Plan-based scheduling is a plug-in for CQsim. Given the current system state consisting of the start time, the expected runtime, and 
the resource usage for each running job, the plan-based scheduler should generate an execution plan for the jobs in the waiting queue that 
assigns each waiting job a start time in order to minimize certain performance metric. Since the CQsim is queue-based scheduling, 
the waiting jobs are extracted from the job execution plan to the execution queue sorted by their planned start times, allowing the HPC 
system to start a job at the head of the executing queue when its planned start time arrives.

The RS scheduling algorithm is for fair comparison as an alternative plan-based scheduling. The difference between RS and our plan-based 
scheduling is the "annealing" part. The RS don't contain the temperature as the annealing, and would work as a local search algorithm.
