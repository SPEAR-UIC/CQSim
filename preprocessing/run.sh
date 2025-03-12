#!/bin/bash

# Run preprocessing scripts
python3 preprocessing_polaris_23_24.py
python3 preprocessing_theta_23_24.py
python3 combine_polaris_theta_23.py 


# Run tests
python3 test.py output/polaris_23.swf
python3 test.py output/theta_23.swf
python3 test.py output/polaris_theta_23.swf