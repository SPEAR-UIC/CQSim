import optparse
import os
import sys
from datetime import datetime
import time
import re
import cqsim_path
import cqsim_main

def datetime_strptime (value, format):
    """Parse a datetime like datetime.strptime in Python >= 2.5"""
    return datetime(*time.strptime(value, format)[0:6])

class Option (optparse.Option):
    
    """An extended optparse option with cbank-specific types.
    
    Types:
    date -- parse a datetime from a variety of string formats
    """
    
    DATE_FORMATS = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%y-%m-%d",
        "%y-%m-%d %H:%M:%S",
        "%y-%m-%d %H:%M",
        "%m/%d/%Y",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M",
        "%m/%d/%y",
        "%m/%d/%y %H:%M:%S",
        "%m/%d/%y %H:%M",
        "%Y%m%d",
    ]
    
    def check_date (self, opt, value):
        """Parse a datetime from a variety of string formats."""
        for format in self.DATE_FORMATS:
            try:
                dt = datetime_strptime(value, format)
            except ValueError:
                continue
            else:
                # Python can't translate dates before 1900 to a string,
                # causing crashes when trying to build sql with them.
                if dt < datetime(1900, 1, 1):
                    raise optparse.OptionValueError(
                        "option %s: date must be after 1900: %s" % (opt, value))
                else:
                    return dt
        raise optparse.OptionValueError(
            "option %s: invalid date: %s" % (opt, value))
    
    TYPES = optparse.Option.TYPES + ( "date", )
    
    TYPE_CHECKER = optparse.Option.TYPE_CHECKER.copy()
    TYPE_CHECKER['date'] = check_date

def callback_alg (option, opt_str, value, parser):
    temp_opt['alg'].append(value)
    return
def callback_alg_sign (option, opt_str, value, parser):
    temp_opt['alg_sign'].append(value)
    return
def callback_bf_para (option, opt_str, value, parser):
    temp_opt['bf_para'].append(value)
    return
def callback_win_para (option, opt_str, value, parser):
    temp_opt['win_para'].append(value)
    return
def callback_ad_win_para (option, opt_str, value, parser):
    temp_opt['ad_win_para'].append(value)
    return
def callback_ad_bf_para (option, opt_str, value, parser):
    temp_opt['ad_bf_para'].append(value)
    return
def callback_ad_alg_para (option, opt_str, value, parser):
    temp_opt['ad_alg_para'].append(value)
    return

def get_raw_name (file_name):
    output_name = ""
    length = len(file_name)
    i = 0
    while (i < length):
        if (file_name[i] == '.'):
            break
        output_name+=file_name[i]
        i += 1
    return output_name

def alg_sign_check (alg_sign_t,leng):
    alg_sign_result=[]
    temp_len=len(alg_sign_t)
    i=0
    while i<leng:
        if i<temp_len:
            alg_sign_result.append(int(alg_sign_t[i]))
        else:
            #alg_sign_result.append(int(alg_sign_t[temp_len-1]))
            alg_sign_result.append(0)
        i+=1
    return alg_sign_result

def get_list (inputstring,regex):
    return re.findall(regex,inputstring)

def read_config(fileName):
    nr_sign =';'    # Not read sign. Mark the line not the job data
    sep_sign ='='   # The sign seperate data in a line
    readData={}
    configFile = open(fileName,'r')

    while (1):
        tempStr = configFile.readline()
        if not tempStr :    # break when no more line
            break
        if tempStr[0] != nr_sign:   # The job trace line
            strNum = len(tempStr)
            newWord = 1
            k = 0
            dataName = ""
            dataValue = ""     
            
            for i in range(strNum):
                if (tempStr[i] == '\n'):
                    break
                if (tempStr[i] == sep_sign):
                    if (newWord == 0):
                        newWord = 1
                        k = k+1
                else:
                    newWord = 0
                    if k == 0:
                        dataName=dataName+ tempStr[i] 
                    elif k == 1:
                        dataValue = dataValue + tempStr[i] 
            readData[dataName]=dataValue
    configFile.close()
    
    return readData


if __name__ == "__main__":
    
    temp_opt={'alg':[],'alg_sign':[],'bf_para':[],'win_para':[],'ad_win_para':[],'ad_bf_para':[],'ad_alg_para':[]}
    p = optparse.OptionParser(option_class=Option)
    # 1
    p.add_option("-j", "--job", dest="job_trace", type="string", \
        help="file name of the job trace")
    p.add_option("-n", "--node", dest="node_struc", type="string", \
        help="file name of the node structure")
    p.add_option("-J", "--job_save", dest="job_save", type="string", \
        help="file name of the formatted job data")
    p.add_option("-N", "--node_save", dest="node_save", type="string", \
        help="file name of the formatted node data")
    p.add_option("-f", "--frac", dest="cluster_fraction", type="float", \
        #default=1.0, \
        help="job density adjust")
        
    # 6
    p.add_option("-s", "--start", dest="start", type="float", \
        #default=0.0, \
        help="virtual job trace start time")
    p.add_option("-S", "--start_date", dest="start_date", type="date", \
        help="job trace start date")
    p.add_option("-r", "--anchor", dest="anchor", type="int", \
        #default=0, \
        help="first read job position in job trace")
    p.add_option("-R", "--read", dest="read_num", type="int", \
        #default=-1, \
        help="number of jobs read from the job trace")
    p.add_option("-p", "--pre", dest="pre_name", type="string",\
        #default="CQSIM_", \
        help="previous file name")
        
    # 11
    p.add_option("-o", "--output", dest="output", type="string",\
        help="simulator result file name")
    p.add_option("--debug", dest="debug", type="string",\
        help="debug file name")
    p.add_option("--ext_fmt_j", dest="ext_fmt_j", type="string",\
        #default=".csv", \
        help="temp formatted job data extension type")
    p.add_option("--ext_fmt_n", dest="ext_fmt_n", type="string",\
        #default=".csv", \
        help="temp formatted node data extension type")
    p.add_option("--ext_fmt_j_c", dest="ext_fmt_j_c", type="string",\
        #default=".con", \
        help="temp job trace config extension type")
        
    # 16
    p.add_option("--ext_fmt_j_n", dest="ext_fmt_n_c", type="string",\
        #default=".con", \
        help="temp job trace config extension type")
    p.add_option("--path_in", dest="path_in", type="string",\
        #default="Input Files/", \
        help="input file path")
    p.add_option("--path_out", dest="path_out", type="string",\
        #default="Results/", \
        help="output result file path")
    p.add_option("--path_fmt", dest="path_fmt", type="string",\
        #default="Temp/", \
        help="temp file path")
    p.add_option("--path_debug", dest="path_debug", type="string",\
        #default="Debug/", \
        help="debug file path")
        
    # 21
    p.add_option("--ext_jr", dest="ext_jr", type="string",\
        #default=".rst", \
        help="job result log extension type")
    p.add_option("--ext_si", dest="ext_si", type="string",\
        #default=".ult", \
        help="system information log extension type")
    p.add_option("--ext_ai", dest="ext_ai", type="string",\
        #default=".adp", \
        help="adapt information log extension type")
    p.add_option("--ext_d", dest="ext_debug", type="string",\
        #default=".log", \
        help="debug log extension type")
    p.add_option("-v", "--debug_lvl", dest="debug_lvl", type="int",\
        #default=4, \
        help="debug mode")
        
    # 26
    p.add_option("-a", "--alg", dest="alg", type="string",\
        action="callback", callback=callback_alg,\
        help="basic algorithm list")
    p.add_option("-A", "--sign", dest="alg_sign", type="string",\
        action="callback", callback=callback_alg_sign,\
        help="sign of the algorithm element in the list")
    p.add_option("-b", "--bf", dest="backfill", type="int",\
        #default=0, \
        help="backfill mode")
    p.add_option("-B", "--bf_para", dest="bf_para", type="string",\
        action="callback", callback=callback_bf_para,\
        help="backfill parameter list")
    p.add_option("-w", "--win", dest="win", type="int",\
        #default=0, \
        help="window mode")
        
    # 31
    p.add_option("-W", "--win_para", dest="win_para", type="string",\
        action="callback", callback=callback_win_para,\
        help="window parameter list")
    p.add_option("-l", "--ad_bf", dest="ad_bf", type="int",\
        #default=0, \
        help="backfill adapt mode")
    p.add_option("-L", "--ad_bf_para", dest="ad_bf_para", type="string",\
        action="callback", callback=callback_ad_bf_para,\
        help="backfill adapt parameter list")
    p.add_option("-d", "--ad_win", dest="ad_win", type="int",\
        #default=0, \
        help="window adapt mode")
    p.add_option("-D", "--ad_win_para", dest="ad_win_para", type="string",\
        action="callback", callback=callback_ad_win_para,\
        help="window adapt parameter list")
        
    # 36
    p.add_option("-g", "--ad_alg", dest="ad_alg", type="int",\
        #default=0, \
        help="algorithm adapt mode")
    p.add_option("-G", "--ad_alg_para", dest="ad_alg_para", type="string",\
        action="callback", callback=callback_ad_alg_para,\
        help="algorithm adapt parameter list")
    p.add_option("-c", "--config_n", dest="config_n", type="string",\
        default="config_n.set", \
        help="name config file")
    p.add_option("-C", "--config_sys", dest="config_sys", type="string",\
        default="config_sys.set", \
        help="system config file")
    p.add_option("-m", "--monitor", dest="monitor", type="int",\
        help="monitor interval time")

    #41
    p.add_option("-I", "--log_freq", dest="log_freq", type="int",\
        help="log frequency")

    p.add_option("-z", "--read_input_freq", dest="read_input_freq", type="int",\
        help="read input frequency")
        
        
    opts, args = p.parse_args()

    inputPara={}
    inputPara_sys={}
    inputPara_name={}
    opts.alg = temp_opt['alg']
    opts.alg_sign = temp_opt['alg_sign']
    opts.bf_para = temp_opt['bf_para']
    opts.win_para = temp_opt['win_para']
    opts.ad_win_para = temp_opt['ad_win_para']
    opts.ad_bf_para = temp_opt['ad_bf_para']
    opts.ad_alg_para = temp_opt['ad_alg_para']
        
    inputPara['resource_job']=0
    inputPara['resource_node']=0
    # 0:Read original file   1:Read formatted file
    
    
    
    
    
    if opts.config_sys:
        inputPara_sys = read_config(cqsim_path.path_config+opts.config_sys) 
    if opts.config_n:
        inputPara_name = read_config(cqsim_path.path_config+opts.config_n)
    elif inputPara_sys['config_n']:
        opts.config_n=inputPara_sys['config_n']
        inputPara_name = read_config(opts.config_n)
        
    if not opts.job_trace and inputPara_sys["job_trace"]:
        opts.job_trace = inputPara_sys["job_trace"]
        
    if not opts.node_struc  and not inputPara_sys["node_struc"]:
        opts.node_struc = inputPara_sys["node_struc"]
        
    if not opts.job_trace and not opts.job_save and not inputPara_sys["job_trace"]:
        print("Error: Please specify an original job trace or a formatted job data!")
        p.print_help()
        sys.exit()
    if not opts.node_struc and not opts.node_save and not inputPara_sys["node_struc"]:
        print("Error: Please specify an original node structure or a formatted node data!")
        p.print_help()
        sys.exit()
    if not opts.alg and not inputPara_sys["alg"]:
        print("Error: Please specify the algorithm element!")
        p.print_help()
        sys.exit()
        
    if not opts.job_trace:
        inputPara['resource_job']=1
    if not opts.node_struc:
        inputPara['resource_node']=1
    if not opts.output:
        opts.output = get_raw_name(opts.job_trace)
    if not opts.debug:
        opts.debug = "debug_"+get_raw_name(opts.job_trace)
    if not opts.job_save:
        opts.job_save = get_raw_name(opts.job_trace)
    if not opts.node_save:
        opts.node_save = get_raw_name(opts.job_trace)+"_node"
    if not opts.bf_para:
        opts.bf_para = []
    if not opts.ad_win_para:
        opts.ad_win_para = []
    if not opts.ad_bf_para:
        opts.ad_bf_para = []
    if not opts.ad_alg_para:
        opts.ad_alg_para = []
    if not opts.log_freq:
        opts.log_freq = 1
    if not opts.read_input_freq:
        opts.read_input_freq = 1000
    '''
    if not opts.job_save:
        print "Error: Please specify at least one node structure!"
        p.print_help()
        sys.exit()
    '''
        
    inputPara['job_trace']=opts.job_trace
    inputPara['node_struc']=opts.node_struc
    inputPara['job_save']=opts.job_save
    inputPara['node_save']=opts.node_save
    inputPara['cluster_fraction']=opts.cluster_fraction
    inputPara['start']=opts.start
    inputPara['start_date']=opts.start_date
    inputPara['anchor']=opts.anchor
    inputPara['read_num']=opts.read_num
    inputPara['pre_name']=opts.pre_name
    inputPara['output']=opts.output
    inputPara['debug']=opts.debug
    inputPara['ext_fmt_j']=opts.ext_fmt_j
    inputPara['ext_fmt_n']=opts.ext_fmt_n
    inputPara['ext_fmt_j_c']=opts.ext_fmt_j_c
    inputPara['ext_fmt_n_c']=opts.ext_fmt_n_c
    inputPara['path_in']=opts.path_in
    inputPara['path_out']=opts.path_out
    inputPara['path_fmt']=opts.path_fmt
    inputPara['path_debug']=opts.path_debug
    inputPara['ext_jr']=opts.ext_jr
    inputPara['ext_si']=opts.ext_si
    inputPara['ext_ai']=opts.ext_ai
    inputPara['ext_debug']=opts.ext_debug
    inputPara['debug_lvl']=opts.alg
    inputPara['alg']=opts.alg
    inputPara['alg_sign']=opts.alg_sign
    inputPara['backfill']=opts.backfill
    inputPara['bf_para']=opts.bf_para
    inputPara['win']=opts.win
    inputPara['win_para']=opts.win_para
    inputPara['ad_win']=opts.ad_win
    inputPara['ad_win_para']=opts.ad_win_para
    inputPara['ad_bf']=opts.ad_bf
    inputPara['ad_bf_para']=opts.ad_bf_para
    inputPara['ad_alg']=opts.ad_alg
    inputPara['ad_alg_para']=opts.ad_alg_para
    inputPara['config_n']=opts.config_n
    inputPara['config_sys']=opts.config_sys
    inputPara['monitor']=opts.monitor
    inputPara['log_freq']=opts.log_freq
    inputPara['read_input_freq']=opts.read_input_freq

    for item in inputPara_name:
        if not inputPara[item]:
            inputPara[item]=str(inputPara_name[item])
            
    for item in inputPara_sys:
        if not inputPara[item]:
            if inputPara_sys[item]:
                if item=="cluster_fraction" or \
                   item=="start": 
                    inputPara[item]=float(inputPara_sys[item])
                elif item=="start_date" :
                    inputPara[item]=str(inputPara_sys[item])
                elif item=="anchor" or \
                   item=="read_num" or \
                   item=="backfill" or \
                   item=="win" or \
                   item=="debug_lvl" or \
                   item=="ad_bf" or \
                   item=="ad_win" or \
                   item=="ad_alg" or \
                   item=="monitor":
                    inputPara[item]=int(inputPara_sys[item])
                elif item=="alg" or \
                   item=="alg_sign" or \
                   item=="bf_para" or \
                   item=="win_para" or \
                   item=="ad_win_para" or \
                   item=="ad_bf_para" or \
                   item=="ad_alg_para":
                    inputPara[item]=get_list(inputPara_sys[item],r'([^,]+)')
                else:  
                    inputPara[item]=str(inputPara_sys[item])
            else:
                inputPara[item]=None
                
            
    

    inputPara['path_in']=cqsim_path.path_data+inputPara['path_in']
    inputPara['path_out']=cqsim_path.path_data+inputPara['path_out']
    inputPara['path_fmt']=cqsim_path.path_data+inputPara['path_fmt']
    inputPara['path_debug']=cqsim_path.path_data+inputPara['path_debug']
    inputPara['alg_sign']=alg_sign_check(inputPara['alg_sign'],len(inputPara['alg']))
    cqsim_main.cqsim_main(inputPara)
