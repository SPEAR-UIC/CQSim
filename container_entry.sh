#!/bin/bash

###########################################
# Preprocess log data
cd preprocessing
echo "Time Zone Date"
date
echo "Unzipping data"
unzip data.zip

# This will create the preprocessing/output directory in the container
# for SWF files for the simualtor
./run.sh
cd ..

###########################################
# Run CQSim+ for experiments and case study
cd src
python3 experiments.py
cd ..

###########################################
# Create the plots
cd plot
python3 plot_main.py
cd ..

###########################################
# Copy the reproduced results outside of container
cp -r /cqsimplus/data /reproduced_results/
cp -r /cqsimplus/preprocessing/output/* /reproduced_results/data/InputFiles/
cp -r /cqsimplus/plot/reproduced/experiments /reproduced_results/
cp -r /cqsimplus/plot/reproduced/case_study /reproduced_results/