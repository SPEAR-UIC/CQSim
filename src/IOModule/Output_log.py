import IOModule.Log_print as Log_print

__metaclass__ = type

class Output_log:
    def __init__(self, output = None):
        self.myInfo = "Output_log"
        self.output_path = output
        self.reset_output()
    
    def reset(self, output = None):
        if output:
            self.output_path = output
            self.reset_output()

    def reset_output(self):   
        self.sys_info = Log_print.Log_print(self.output_path['sys'],0)
        self.sys_info.reset(self.output_path['sys'],0)
        self.sys_info.file_open()
        self.sys_info.file_close()
        self.sys_info.reset(self.output_path['sys'],1)   
        
        self.adapt_info = Log_print.Log_print(self.output_path['adapt'],0)
        self.adapt_info.reset(self.output_path['adapt'],0)
        self.adapt_info.file_open()
        self.adapt_info.file_close()
        self.adapt_info.reset(self.output_path['adapt'],1)
        
        self.job_result = Log_print.Log_print(self.output_path['result'],0)
        self.job_result.reset(self.output_path['result'],0)
        self.job_result.file_open()
        self.job_result.file_close()
        self.job_result.reset(self.output_path['result'],1)              
        
    def print_sys_info(self, sys_info):
        sep_sign=";"
        sep_sign_B=" "
        sep_sign_C="\t"
        context = ""
        '''
        context += str(sys_info['date'])
        context += sep_sign
        context += str(sys_info['event'])
        context += sep_sign
        context += str(sys_info['time'])
        context += sep_sign
        
        context += ('uti'+'='+str(sys_info['uti']))
        context += sep_sign_B
        context += ('waitTime'+'='+str(sys_info['waittime']))
        context += sep_sign_B
        context += ('slowdown'+'='+str(sys_info['slowdown']))
        context += sep_sign_B
        context += ('avgUti'+'='+str(sys_info['avg_uti'][0]))
        
        self.sys_info.file_open()
        self.sys_info.log_print(context,1)
        self.sys_info.file_close()
        '''
        if (sys_info['event'] != 'S' and sys_info['event'] != 'Q' and sys_info['event'] != 'E' ):
            context += str(sys_info['time']*1.0/2592000)
            context += sep_sign_C
            context += str(sys_info['job_submit'])
            context += sep_sign_C
            context += str(sys_info['job_start'])
            context += sep_sign_C
            context += str(sys_info['job_end'])
            context += sep_sign_C
            context += str(sys_info['ave_uti'])
            context += sep_sign_C
            context += str(sys_info['waittime_s'])
            context += sep_sign_C
            context += str(sys_info['waittime_e'])
            context += sep_sign_C
            context += str(sys_info['slowdown'])
            context += sep_sign_C
            context += str(sys_info['queue_depth'])
            context += sep_sign_C
            context += str(sys_info['tot_uti'])
            self.sys_info.file_open()
            self.sys_info.log_print(context,1)
            self.sys_info.file_close()
        '''
        context += str(sys_info['event'])
        self.sys_info.file_open()
        self.sys_info.log_print(context,1)
        self.sys_info.file_close()
        '''
        
    def print_adapt(self, adapt_info):
        sep_sign=";"
        context = ""
        
        i = 0
        adapt_num = len(adapt_info)
        while (i < adapt_num):
            context += str(adapt_info[i])
            context += sep_sign
            i += 1
        self.adapt_info.file_open()
        self.adapt_info.log_print(context,1)
        self.adapt_info.file_close()
    
    def print_result(self, job_module):
        sep_sign=";"
        context = ""
        self.job_result.file_open()
        i = 0
        done_list = job_module.done_list()
        job_num = len(done_list)
        
        while (i<job_num):
            temp_job = job_module.job_info(i)
            context = ""
            context += str(temp_job['id'])
            context += sep_sign
            context += str(temp_job['reqProc'])
            context += sep_sign
            context += str(temp_job['reqProc'])
            context += sep_sign
            context += str(temp_job['reqTime'])
            context += sep_sign
            context += str(temp_job['run'])
            context += sep_sign
            context += str(temp_job['wait'])
            context += sep_sign
            context += str(temp_job['submit'])
            context += sep_sign
            context += str(temp_job['start'])
            context += sep_sign
            context += str(temp_job['end'])
            #context += sep_sign
            #context += str(temp_job['nodeList'])
            self.job_result.log_print(context,1)
            
            i += 1
            
        self.job_result.file_close()