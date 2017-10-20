'''factory import'''

# Original class ################################################
from Filter import Filter_job as Class_Filter_job
from Filter import Filter_node as Class_Filter_node
from CqSim import Job_trace as Class_Job_trace
from CqSim import Node_struc as Class_Node_struc

from CqSim import Backfill as Class_Backfill
from CqSim import Start_window as Class_Start_window
from CqSim import Basic_algorithm as Class_Basic_algorithm
from CqSim import Info_collect as Class_Info_collect
from CqSim import Cqsim_sim as Class_Cqsim_sim

from IOModule import Debug_log as Class_Debug_log
from IOModule import Output_log as Class_Output_log


# SWF ###########################################################
from Extend.SWF import Filter_job_SWF as Class_Filter_job_SWF
from Extend.SWF import Filter_node_SWF as Class_Filter_node_SWF



factory_list = {}

factory_list['ORG'] = {'f_job':Class_Filter_job.Filter_job, \
                       'f_node':Class_Filter_node.Filter_node, \
                       'job':Class_Job_trace.Job_trace, \
                       'node':Class_Node_struc.Node_struc, \
                       'backfill':Class_Backfill.Backfill, \
                       'win':Class_Start_window.Start_window, \
                       'alg':Class_Basic_algorithm.Basic_algorithm, \
                       'info':Class_Info_collect.Info_collect, \
                       'sim':Class_Cqsim_sim.Cqsim_sim, \
                       'debug':Class_Debug_log.Debug_log, \
                       'output':Class_Output_log.Output_log, \
                       }


factory_list['SWF'] = {'f_job':Class_Filter_job_SWF.Filter_job_SWF, \
                       'f_node':Class_Filter_node_SWF.Filter_node_SWF, \
                       'job':Class_Job_trace.Job_trace, \
                       'node':Class_Node_struc.Node_struc, \
                       'backfill':Class_Backfill.Backfill, \
                       'win':Class_Start_window.Start_window, \
                       'alg':Class_Basic_algorithm.Basic_algorithm, \
                       'info':Class_Info_collect.Info_collect, \
                       'sim':Class_Cqsim_sim.Cqsim_sim, \
                       'debug':Class_Debug_log.Debug_log, \
                       'output':Class_Output_log.Output_log, \
                       }
