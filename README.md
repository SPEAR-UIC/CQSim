# CQSim - a discrete-event driven scheduling simulator
CQSim is an open-source, discrete-event driven cluster scheduling simulator. It was originated from QSim, an discrete-event driven scheduling simulator developed for the production batch scheduler Cobalt deployed at Argonne Leadership Computing Facility in 2009 [3]. In 2011-2012, Qsim was evolved into CQSim by adding more functionalities and features. CQSim was originally developed by Dongxu Ren and Wei Tang (version 1.0), and later was improved by Xu Yang and Yuping Fan (master branch) [1,2], all under the supervision of Zhiling Lan.  

CQSim is written in Python, and is formed by several modules including job module, node module, scheduling policy module, etc. Each module is implemented as a class. Its design principles are reusability, extensibility, and efficiency. CQSim takes job events from a workload trace (e.g., the SWF format from Parallel Workload Archive. Based on the events, the simulator emulates job submission, allocation, and execution according to a specific scheduling policy. 

CQSim has been extensively validated by comparing its simulation results with the real system traces listed in the well-known Parallel Workload Archive (https://www.cs.huji.ac.il/labs/parallel/workload/). It was also assessed with the scheduling simulator developed by Dan Tsafrir. A number of system-level and user-level metrics, e.g., makespan, system utilization rate, job wait time, job slowdown, etc., were used in the quantitative validation.  

Note: if you use CQSim in your work, please cite the following papers: 
1. X. Yang, Z. Zhou, S. Wallace, Z. Lan, W. Tang, S. Coghlan, and M. Papka, "Integrating Dynamic Pricing of Electricity into Energy Aware Scheduling for HPC Systems", Proc. of SC'13, 2013.[http://www.cs.iit.edu/~lan/publications/sc13_final.pdf]
2. Y. Fan, Z. Lan, P. Rich, W. Allcock, M. Papka, B. Austin, and D. Paul, "Scheduling beyond CPUs for HPC", Proc. of HPDC'19, 2019. [http://www.cs.iit.edu/~lan/publications/hpdc19-final.pdf]
3. W. Tang, Z. Lan, N. Desai, and D. Buettner, “Fault-aware Utility-based Job Scheduling on Blue Gene/P Systems,” Proc of IEEE Cluster, 2009. [http://www.cs.iit.edu/~lan/publications/ipdps11_wei.pdf]

# Getting started: Run A Simple Example
```
python cqsim.py -j test.swf -n test.swf
```
