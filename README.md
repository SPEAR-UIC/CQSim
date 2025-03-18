# Reproducibility PADS 2025

This document describes how to reproduce the results discussed in the paper:

"CQSim+: Symbiotic Simulation for Multi-Resource Scheduling in High-Performance Computing"

Accepted to ACM SIGSIM PADS 2025

Public repository can be found at: https://github.com/SPEAR-UIC/CQSim/tree/CQSimPlus

## Authors & Contacts

* Yash Kurkure <ykurku2@uic.edu>
* Shambhawi Sharma <sshar102@uic.edu>
* Xin Wang <xwang823@uic.edu>
* Michael E. Papka <papka@uic.edu>
* Zhilling Lan <zlan@uic.edu>

Contact for reproducibility: Yash Kurkure <ykurku2@uic.edu>clear

## Requirements

* Preferably Linux or MacOS
* Minimum 8GB of RAM

The hardware/software configuration used by the authors is:

* CPU: Apple Silicon M2
* RAM: 8 GB
* OS: Mac OS Sequoia 15.3.1 + Docker (Fedora 40)


## Dependencies
All code is run inside a docker container. The docker file to build the image can be found in the artifact. 
* Docker Engine
* Docker CLI

## License

The software is released with the MIT license.


## Reproducing the results

For reproducing the results from the paper, a Dockerfile is provided that mimicks the exact environment the experiments were conducted in. So make sure your system has docker installed.

### Linux/MacOS
- Step 1: Run `reproduce.sh` which will run all experiments in a docker container. At the end of execution, look for the folder `reproduced_results`. This folder will contain all table and graph data used in the paper.

### Windows

- Step 1: Run `dos2unix reproduce.sh` and `dos2unix preprocessing/run.sh`. This is required for gitbash as windows requires a different new line character.

- Step 3: Run `reproduce.sh` which will run all experiments in a docker container. At the end of execution, look for the folder `reproduced_results`. This folder will contain all table and graph data used in the paper.

Expect the script to run for a minimum of 50 mins to 1hr 15 mins depending on your machine

## Reproduced Directory

Once all experiments have been run, you can find all the reproduced results in the `reproduced_results` directory.

### Overview

The `reproduced_results` has three sub directories:
- data: Contains data produced from the simulations
- experiments: Figures and tables plotted for the homogeneous and heterogeneous experiments
- case_study: Figures and tables plotted for the case study 
```
reproduced_results/
│   ├── case_study/ /* Figures and tables for case study */
│   ├── data/
│   │   ├── InputFiles/
│   │   └── Results/
│   │       ├── exp_polaris_theta/ /*Data for case study simulation*/
│   │       │   ├── only_polaris/ /*Data for siloed Polaris scheduling*/
│   │       │   ├── only_theta/ /*Data for siloed Theta scheduling*/
│   │       │   └── sgst/ /*Data for multi resource scheduling Polaris and Theta*/
│   │       │       ├── jobs.csv
│   │       │       ├── performance.csv
│   │       │       ├── polaris/ /*Polaris data*/
│   │       │       └── theta/ /*Theta data*/
│   │       └── exp_theta_two_parts/ /*Data for experiment simulation*/
│   │           ├── optimal_turnaround_1/ /*Data for homogeneous case SGST*/
│   │           │   ├── cluster_1/
│   │           │   ├── cluster_2/
│   │           │   └── theta/
│   │           ├── optimal_turnaround_1.3/ /*Data for heterogeneous case SGS-T*/
│   │           │   ├── cluster_1/
│   │           │   ├── cluster_2/ /*Cluster 2 runs speed of 1.3x of Cluster 1*/
│   │           │   └── theta/
│   │           ├── probable_user_1.3_0.6/ /*Data for heterogeneous case User(0.6)*/
│   │           │   ├── cluster_1/
│   │           │   ├── cluster_2/ /*Cluster 2 runs speed of 1.3x of Cluster 1*/
│   │           │   └── theta/
│   │           └── probable_user_1_0.5 /*Data for homogeneous case Random*/
│   │               ├── cluster_1/
│   │               ├── cluster_2/
│   │               └── theta/
│   └── experiments/ /*Figures and tables for experiments*/
```
### Figures and Tables

| Table      | Path |
|--------------|---------|
| 1           | reproduced_results/experiments/table1.csv    |
| 2           | reproduced_results/experiments/table2.csv     |
| 3           | reproduced_results/experiments/table3.csv      |
| 4           | reproduced_results/experiments/table4.csv   |
| 5           | reproduced_results/case_study/table5.csv    |

| Figure       | Path |
|--------------|---------|
| 5a           | reproduced_results/experiments/figure5a.png     |
| 5b           | reproduced_results/experiments/figure5b.png    |
| 5c           | reproduced_results/experiments/figure5c.png     |
| 5d           | reproduced_results/experiments/figure5d.png     |
| 6a           | reproduced_results/experiments/figure6a.png   |
| 6b           | reproduced_results/experiments/figure6b.png   |
| 7a           | reproduced_results/case_study/figure7a.png      |
| 7b           | reproduced_results/case_study/figure7b.png  |
| 7c           | reproduced_results/case_study/figure7c.png     |
| 7d           | reproduced_results/case_study/figure7d.png   |
| 8a           | reproduced_results/case_study/figure8a.png   |
| 8b           | reproduced_results/case_study/figure8b.png    |

## Understading the reproducibility scripts

### Preprocessing scripts
The data preporcessing scripts can be found in `preprocessing`. These scripts are responsible for reading the raw cluster logs and converting them to SWF files for the simulator. They read the raw data from `proprocessing/data` and output the preprocessed data into `preprocessing/output` directory. These SWF files are also copied to the `reproduced_results/data/InputFiles` for the reviewers to examine if needed.

### Simulation scripts
The simulation scripts can be found under `src`. The main script to run all simulations is `experiments.py` which runs all experiments in parallel.

This script imports from two main files: `exp_theta_two_parts.py` and `exp_polaris_theta.py`. The first runs the expeeriments for the homogeneous and heterogenous clustes. The second runs the experiments for the case study.

### Plotting Scripts
All plotting scritps are found in `plot`. These scripts read the data that is output by the simulator. The output data used by these can be found under `reproduced_results/data/Results`

Each script is named in accordance to the name of the figure or table it produces. The `plot_main.py` script imports the individual fucntions responsible for plotting each figure and table. 

### reporoduce.sh
The main script that builds the docker container and sets up the external directory so that the results can be copied outside of the container.

### Dockerfile
This files configures the container's environment and installs all dependencies.

### container_entry.sh
This script is run inside the docker container. It contains all the commands required to run the simulator, plot the data, and copy the data from inside of the container to the outside under `reproduced_results`

## Note

Some values in the tables may not be exact to those in the paper as averages of multiple runs under randomness were taken into account.
The results can be averaged by running the `./reproduce.sh` script multiple times if needed.