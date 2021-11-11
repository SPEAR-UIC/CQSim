# DRAS - Deep Reinforcement Learning Agent for Scheduling in HPC
This is the implementation of DRAS in CQSim simulator.


More details is available and if you use DRAS in your work, please cite the following paper:

Y. Fan, T. Childers, P. Rich, W. Allcock, M. Papka, and Z. Lan, "Deep Reinforcement Agent for Scheduling in HPC", Proc. of IPDPS'21, 2021.[http://cs.iit.edu/~lan/publications/DRAS-ipdps2021.pdf]

# Run A Simple Example
## Train DRAS with 100 jobs
Modify two parameters in CQSim/PG/Config/config_sys.set file:
```
read_num=100
is_training=1
```
Run:
```
python cqsim.py -j test.swf -n test.swf
```

## Test DRAS after training
Modify CQSim/PG/Config/config_sys.set file:
```
is_training=0
```

Run:
```
python cqsim.py -j test.swf -n test.swf
```

Output are in ```data/Results```.
