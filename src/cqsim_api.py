from cqsim_main import cqsim_main
from CqSim.Cqsim_sim import time_stamps

def simulate(
        job_trace,
        node_struc,
        debug_lvl=3,
        path_in = ".",
        path_out = ".",
        path_fmt = ".",
        path_debug = ".",
        output = "test",
        debug = "debug_test",
):

    para_list = build_para_list(
        resource_job = 0,
        resource_node = 0,
        job_trace = job_trace,
        node_struc = node_struc,
        job_save = "test",
        node_save = "test_node",
        cluster_fraction = 1.0,
        start = 0.0,
        start_date = None,
        anchor = 0,
        read_num = 8000,
        pre_name = "CQSIM_",
        output = output,
        debug = debug,
        ext_fmt_j = ".csv",
        ext_fmt_n = ".csv",
        ext_fmt_j_c = ".con",
        ext_fmt_n_c = ".con",
        path_in = path_in,
        path_out = path_out,
        path_fmt = path_fmt,
        path_debug = path_debug,
        ext_jr = ".rst",
        ext_si = ".ult",
        ext_ai = ".adp",
        ext_debug = ".log",
        debug_lvl = debug_lvl,
        alg = ['w', '+', '2'],
        alg_sign = [1, 0, 1],
        backfill = 2,
        bf_para = None,
        win = 5,
        win_para = ['5', '0', '0'],
        ad_win = 0,
        ad_win_para = None,
        ad_bf = 0,
        ad_bf_para = ['ad_bf_para.set'],
        ad_alg = 0,
        ad_alg_para = None,
        config_n = "config_n.set",
        config_sys = "config_sys.set",
        monitor = 500,
        log_freq = 1,
        read_input_freq = 1000)
    
    module_list = cqsim_main(para_list)
    if module_list is None:
        return []

    return module_list

def build_para_list(** kwargs):
    return kwargs

if __name__ == "__main__": 
    simulate(
                path_in = "../data/InputFiles/",
                path_out = "../data/Results/",
                path_fmt = "../data/Fmt/",
                path_debug = "../data/Debug/",
                job_trace= "test.swf",
                node_struc= "test.swf",
                debug_lvl=4)