#!/bin/bash

###########################################
# Preprocess log data
cd preprocessing
# This will create the preprocessing/output directory container SWF files for the simualtor
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
python3 case_study.py
python3 experiments.py

cd ..

###########################################
# Copy the reproduced results outside of container
cp -r /cqsimplus/plot/reproduced/experiments /reproduced_results/
cp -r /cqsimplus/plot/reproduced/case_study /reproduced_results/