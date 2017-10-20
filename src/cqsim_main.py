import cqsim_path
import Factory
from datetime import datetime
import time

def  cqsim_main(para_list):
    start_time = datetime.now()
    print "...................."
    for item in para_list :
        print str(item) + ": " + str(para_list[item])
    print "...................."
        
    trace_name = para_list['path_in'] + para_list['job_trace']
    save_name_j = para_list['path_fmt'] + para_list['job_save'] + para_list['ext_fmt_j'] 
    config_name_j = para_list['path_fmt'] + para_list['job_save'] + para_list['ext_fmt_j_c'] 
    struc_name = para_list['path_in'] + para_list['node_struc']
    save_name_n = para_list['path_fmt'] + para_list['node_save'] + para_list['ext_fmt_n'] 
    config_name_n = para_list['path_fmt'] + para_list['node_save'] + para_list['ext_fmt_n_c'] 
    
    output_sys = para_list['path_out'] + para_list['output'] + para_list['ext_si']
    output_adapt = para_list['path_out'] + para_list['output'] + para_list['ext_ai']
    output_result = para_list['path_out'] + para_list['output'] + para_list['ext_jr']
    output_fn = {'sys':output_sys, 'adapt':output_adapt, 'result':output_result}
    
    modules = Factory.Module_factory(para_list['module_ver'])
    
    # Debug
    print ".................... Debug"
    debug_path = para_list['path_debug'] + para_list['debug'] + para_list['ext_debug']
    module_debug = modules.debug(lvl=para_list['debug_lvl'],show=2,path=debug_path)
    #module_debug.start_debug()
    
    # Node Filter
    print ".................... Node Filter"
    module_filter_node = modules.filter_node(struc=struc_name, save=save_name_n, config=config_name_n, debug=module_debug)
    module_filter_node.read_node_struc()
    module_filter_node.output_node_data()
    module_filter_node.output_node_config()
    temp_max_node = module_filter_node.get_node_num()
    
    # Job Filter
    print ".................... Job Filter"
    module_filter_job = modules.filter_job(trace=trace_name, save=save_name_j, config=config_name_j, sdate=para_list['start_date'], max_node = temp_max_node, debug=module_debug)
    module_filter_job.read_job_trace()
    module_filter_job.output_job_data()
    module_filter_job.output_job_config()
    
    # Job Trace
    print ".................... Job Trace"
    module_job_trace = modules.job(start=para_list['start'],num=para_list['read_num'],anchor=para_list['anchor'],density=para_list['cluster_fraction'],debug=module_debug)
    module_job_trace.import_job_file(save_name_j)
    module_job_trace.import_job_config(config_name_j)
    
    # Node Structure
    print ".................... Node Structure"
    module_node_struc = modules.node(debug=module_debug)
    module_node_struc.import_node_file(save_name_n)
    module_node_struc.import_node_config(config_name_n)
    
    # Information Collect
    print ".................... Information Collect"
    module_info_collect = modules.info (avg_inter=[600,3600],debug=module_debug)
    
    # Backfill
    print ".................... Backfill"
    module_backfill = modules.backfill(mode=para_list['backfill'],ad_mode=para_list['ad_bf'],node_module=module_node_struc,info_module=module_info_collect,debug=module_debug,para_list=para_list['bf_para'],ad_para_list=para_list['ad_bf_para'])
    
    # Start Window
    print ".................... Start Window"
    module_win = modules.start_window(mode=para_list['win'],ad_mode=para_list['ad_win'],node_module=module_node_struc,info_module=module_info_collect,debug=module_debug,para_list=para_list['win_para'],ad_para_list=para_list['ad_win_para'])
    
    # Basic Algorithm
    print ".................... Basic Algorithm"
    module_alg = modules.basic_algorithm (ad_mode=para_list['ad_alg'],element=[para_list['alg'],para_list['alg_sign']],info_module=module_info_collect,debug=module_debug,ad_para_list=para_list['ad_alg_para'])
    
    # Output Log
    print ".................... Output Log"
    module_output_log = modules.output (output=output_fn)
    
    start_time1 = datetime.now()
    # Cqsim Simulator
    print ".................... Cqsim Simulator"
    module_list = {'job':module_job_trace,'node':module_node_struc,'backfill':module_backfill,\
                   'win':module_win,'alg':module_alg,'info':module_info_collect, 'output':module_output_log}
    module_sim = modules.cqsim (module=module_list, debug=module_debug, monitor = para_list['monitor'], mon_para = para_list['mon_para'])
    module_sim.cqsim_sim()
    #module_debug.end_debug()
    finish_time = datetime.now()
    
    module_debug.line(2,"..")
    module_debug.line(2,"..")
    for item in para_list :
        module_debug.debug(str(item) + ": " + str(para_list[item]), 2) 
    module_debug.line(1," ")
    module_debug.line(1,"..")
    module_debug.debug("Total Time: " + str(finish_time-start_time), 1) 
    module_debug.debug("Simulating Time: " + str(finish_time-start_time1), 1) 