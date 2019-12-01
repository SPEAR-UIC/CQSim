# CQSim - A Trace-based Event-Driven Scheduling Simulator
The simulator is written in Python, and is formed by several modules including job module, node module, scheduling policy module, etc. Each module is implemented as a class. Its design principles are reusability, extensibility, and efficiency. CQSim takes job events from a workload trace (e.g., the SWF format from the well-known Parallel Workload Archive at http://www.cs.huji.ac.il/labs/parallel/workload/). Based on the events, the simulator emulates job submission, allocation, and execution according to a specific scheduling policy. 

CQSim was originally developed by Dongxu Ren and Wei Tang (version 1.0) in 2011-2012, and later was improved by Xu Yang and Yuping Fan (master branch), all under the supervision of Zhiling Lan at the Illinois Institute of Technology (http://bluesky.cs.iit.edu/cqsim/). 

Note: if you use CQSim in your work, please cite the paper : X. Yang, Z. Zhou, S. Wallace, Z. Lan, W. Tang, S. Coghlan, and M. Papka, "Integrating Dynamic Pricing of Electricity into Energy Aware Scheduling for HPC Systems", Proc. of SC'13, 2013.

# Getting started: Run A Simple Example
python cqsim.py -j test.swf -n test.swf
