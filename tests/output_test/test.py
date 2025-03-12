"""
This test checks if the output produced by CQSim+ line_step() simulation
alligns with CQSim.

Trace used: theta_1000.rst which containts the first 1000 jobs from theta_2022.rst

- actual.rst contains the output of CQSim+
- expected.rst contains the output of CQSim produced using the command line
"""
import pandas as pd

actual = './actual.rst'
expected = './expected.rst'
column_names = ['id', 'proc1', 'proc2','walltime', 'run', 'wait', 'submit', 'start', 'end']

with open(actual, 'r') as f1, open(expected, 'r') as f2:
    df1 = pd.read_csv(f1, sep=';', header=None, names=column_names)
    df2 = pd.read_csv(f2, sep=';', header=None, names=column_names)


assert(df1.shape == df2.shape)
assert(df1.equals(df2))
