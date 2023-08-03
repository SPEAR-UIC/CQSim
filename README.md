# CQSim - a discrete-event driven scheduling simulator
CQSim is an open-source, discrete-event driven cluster scheduling simulator. It was originated from QSim, an discrete-event driven scheduling simulator developed for the production batch scheduler Cobalt deployed at Argonne Leadership Computing Facility in 2009 [3]. In 2011-2012, Qsim was evolved into CQSim by adding more functionalities and features. CQSim was originally developed by Dongxu Ren and Wei Tang (version 1.0), and later was improved by Xu Yang and Yuping Fan (master branch) [1,2], all under the supervision of Zhiling Lan at Illinois Institute of Technology (http://www.cs.iit.edu/~lan/). 

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

# CQSim GUI

The CQSim GUI is an interactive graphical user interface for CQSim, a simulation program. This GUI provides users with an alternative way to interact with CQSim instead of entering parameters through the terminal. Additionally, it offers the option to view real-time graph analysis while the simulation is running. The GUI allows users to select between graphing Utilization, Max Wait Time, or Average Wait Time of the simulation.

## Running the GUI

To run the CQSim GUI, follow these steps:

1. Make sure you have Python 3 installed on your system.

2. Open a terminal or command prompt.

3. Navigate to the directory where the CQSim files are located.

4. Execute the following command to run the GUI:

```
python3 GUI_cqsim.py
```

## How to Use the GUI

Once you have launched the GUI, you will see a graphical interface with various options and controls.

### Simulation Parameters

The GUI provides input fields and options to set simulation parameters. You can enter these values directly into the provided fields.

### Real-Time Graph Analysis

The GUI allows you to select real-time graph analysis while the simulation is running. You can choose to view graphs for Utilization, Max Wait Time, or Average Wait Time. The graphs will update dynamically as the simulation progresses.

### Interaction with the Simulation

As the simulation is running, the graph pages 'back' button will be grey. When the simulation completes, it will turn blue again. However, if you hit back before the simulation is done, it will stop the simulation in the background as well.


### Additional Notes

- The GUI provides a more user-friendly way to interact with CQSim and visualize simulation results in real-time.

- The GUI_cqsim.py file should be located in the same directory as the CQSim program files to ensure proper execution.

- You can modify the code in GUI_cqsim.py to add more features or customize the user interface based on your requirements.

Enjoy using the CQSim GUI to simulate and analyze queuing systems efficiently! If you encounter any issues or have suggestions for improvement, feel free to contribute or contact the developers.