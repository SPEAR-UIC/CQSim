# CQSim - A Trace-based Event-Driven Scheduling Simulator
The simulator is written in Python, and is formed by several modules including job module, node module, scheduling policy module, etc. Each module is implemented as a class. Its design principles are reusability, extensibility, and efficiency. CQSim takes job events from a workload trace (e.g., the SWF format from the well-known Parallel Workload Archive at http://www.cs.huji.ac.il/labs/parallel/workload/). Based on the events, the simulator emulates job submission, allocation, and execution according to a specific scheduling policy. 

CQSim was originally developed by Dongxu Ren and Wei Tang (version 1.0) in 2011-2012, and later was improved by Xu Yang and Yuping Fan (master branch), all under the supervision of Zhiling Lan at the Illinois Institute of Technology (http://bluesky.cs.iit.edu/cqsim/).

Note: if you use CQSim in your work, please cite the following papers: 
1. X. Yang, Z. Zhou, S. Wallace, Z. Lan, W. Tang, S. Coghlan, and M. Papka, "Integrating Dynamic Pricing of Electricity into Energy Aware Scheduling for HPC Systems", Proc. of SC'13, 2013.
2. Y. Fan, Z. Lan, P. Rich, W. Allcock, M. Papka, B. Austin, and D. Paul, "Scheduling beyond CPUs for HPC", Proc. of HPDC'19, 2019.
3. Y. Fan, T. Childers, P. Rich, W. Allcock, M. Papka, and Z. Lan, "Deep Reinforcement Agent for Scheduling in HPC", Proc. of IPDPS'21, 2021.

# Getting started: Run A Simple Example
```
python cqsim.py -j test.swf -n test.swf
```
