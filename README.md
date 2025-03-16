# Reproducibility PADS 2025

This document describes how to reproduce the results discussed in the paper:

"CQSim+: Symbiotic Simulation for Multi-Resource Scheduling in High-Performance Computing"

Accepted to ACM SIGSIM PADS 2025

## Authors & Contacts

* Yash Kurkure <ykurku2@uic.edu>
* Shambhawi Sharma <sshar102@uic.edu>
* Xin Wang <xwang823@uic.edu>
* Michael E. Papka <papka@uic.edu>
* Zhilling Lan <zlan@uic.edu>

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
- Step 1: Look for the file `preprocessing/data.zip` and Extract this file to `preprocessing/data` OR Download the dataset from [link](https://drive.google.com/drive/folders/1yNwvM4OLp2IND70Fqynq2s8IolcnjPPQ?usp=share_link) and extract the files into `/preprocessing/data`.

- Step 2: Run `reproduce.sh` which will run all experiments in a docker container. At the end of execution, look for the folder `reproduced_results`. This folder will contain all table and graph data used in the paper.

### Windows

- Step 1: Look for the file `preprocessing/data.zip` and Extract this file to `preprocessing/data` OR Download the dataset from [link](https://drive.google.com/drive/folders/1yNwvM4OLp2IND70Fqynq2s8IolcnjPPQ?usp=share_link) and extract the files into `/preprocessing/data`.

- Step 2: Run `dos2unix reproduce.sh` and `dos2unix preprocessing/run.sh`

- Step 3: Run `reproduce.sh` which will run all experiments in a docker container. At the end of execution, look for the folder `reproduced_results`. This folder will contain all table and graph data used in the paper.

Expect the script to run for a minimum of 50 mins to 1hr 15 mins depending on your machine

Once all experiments have been run, you can find each figure and tables at:

| Table      | Path |
|--------------|---------|
| 1           | reproduced_results/experiments/homo_avg_wait_vs_node.csv    |
| 2           | reproduced_results/experiments/homo_avg_wait_vs_walltime.csv     |
| 3           | reproduced_results/experiments/hetero_avg_wait_vs_node.csv      |
| 4           | reproduced_results/experiments/hetero_avg_wait_vs_walltime.csv   |
| 5           | Need to work on this - create a csv     |

| Figure       | Path |
|--------------|---------|
| 5a           | reproduced_results/experiments/homo_avg_uti_random.png     |
| 5b           | reproduced_results/experiments/homo_avg_uti_sgst.png    |
| 5c           | reproduced_results/experiments/homo_jobs_random.png    |
| 5d           | reproduced_results/experiments/homo_jobs_sgst.png    |
| 6a           | reproduced_results/experiments/hetero_avg_uti_random.png    |
| 6b           | reproduced_results/experiments/hetero_avg_uti_sgst.png  |
| 7a           | reproduced_results/case_study/polaris_avg_wait.png     |
| 7b           | reproduced_results/case_study/polaris_jobs.png    |
| 7c           | reproduced_results/case_study/theta_avg_wait.png    |
| 7d           | reproduced_results/case_study/theta_jobs.png   |
| 8a           | reproduced_results/case_study/pot_turnaround.png   |
| 8b           | reproduced_results/case_study/pot_avg_wait.png   |

Todos:
- Table 5 Create csv format
- Fig 5 - Update aggregation for utilization to per week
- Fig 6 - Same as Fig 5
- Fig 7 - Polaris additional bins and siloed scheduling label
- Fig 8 - Siloed scheduling label

## Understanding the scripts

### reporoduce.sh

### Dockerfile

### container_entry.sh

### Experiment Files

### Figure Plotting Scripts

