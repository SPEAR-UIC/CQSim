import os
from table1 import table1
from table2 import table2
from table3 import table3
from table4 import table4
# from table5 import 
from figure_5_6 import *
from figure7 import *


output_exp = 'reproduced/experiments'
output_case = 'reproduced/case_study'
if __name__ == '__main__':

    if not os.path.exists(output_exp):
        os.makedirs(output_exp)

    if not os.path.exists(output_case):
        os.makedirs(output_case)

    # Experiments: Homogeneous and Heterogeneous
    table1()
    table2()
    table3()
    table4()
    figure5a()
    figure5b()
    figure5c()
    figure5d()
    figure6a()
    figure6b()

    # Experiments: Case Study
    figure7a()
    figure7b()
    figure7c()
    figure7d()