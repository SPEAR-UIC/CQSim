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
        '''
        self.avg_dist = Log_print.Log_print(self.output_path['distance'],0)
        self.avg_dist.reset(self.output_path['distance'],0)
        self.avg_dist.file_open()
        self.avg_dist.file_close()
        self.avg_dist.reset(self.output_path['distance'],1)

        self.util_file = Log_print.Log_print(self.output_path['util'],0)
        self.util_file.reset(self.output_path['util'],0)
        self.util_file.file_open()
        self.util_file.file_close()
        self.util_file.reset(self.output_path['util'],1)         

        self.time_file = Log_print.Log_print(self.output_path['time_file'],0)
        self.time_file.reset(self.output_path['time_file'],0)
        self.time_file.file_open()
        self.time_file.file_close()
        self.time_file.reset(self.output_path['time_file'],1)                  
        '''

    def print_sys_info(self, sys_info):
        sep_sign=";"
        sep_sign_B=" "
        context = ""
        context += str(sys_info['date'])
        context += sep_sign
        context += str(sys_info['event'])
        context += sep_sign
        context += str(sys_info['time'])
        context += sep_sign
        
        context += ('uti'+'='+str(sys_info['uti']))
        context += sep_sign_B
        context += ('waitNum'+'='+str(sys_info['waitNum']))
        context += sep_sign_B
        context += ('waitSize'+'='+str(sys_info['waitSize']))
        context += sep_sign_B
        context += ('ran_uti'+'='+str(sys_info['ran_uti']))
        #context += sep_sign_B
        #context += ('ran_power'+'='+str(sys_info['ran_power']))
        self.sys_info.file_open()
        self.sys_info.log_print(context,1)
        self.sys_info.file_close()

    def print_util_list(self, util_list):
        self.util_file.file_open()
        for util in util_list:
            context = ""
            context += str(util)
            self.util_file.log_print(context,1)
        self.util_file.file_close()


    def print_time_list(self, time_list):
            self.time_file.file_open()
            for util in time_list:
                context = ""
                context += str(util)
                self.time_file.log_print(context,1)
            self.time_file.file_close()

    def print_avg_distance(self, avg_distance_list):
        if len(avg_distance_list) > 0:
            self.avg_dist.file_open()
            context = ";"
            context += str(sum(avg_distance_list)/len(avg_distance_list))
            self.avg_dist.log_print(context,1)
            for avg_distance in avg_distance_list:
                context = ""
                context += str(avg_distance)
                self.avg_dist.log_print(context,1)
            self.avg_dist.file_close()
    
    def print_adapt(self, adapt_info):
        sep_sign=";"
        context = ""
        self.adapt_info.file_open()
        self.adapt_info.log_print(context,1)
        self.adapt_info.file_close()
    
    def print_result(self, job_module):
        sep_sign=";"
        context = ""
        self.job_result.file_open()
        fields_str = ""
        fields = ['id','reqProc','reqProc','reqRan','reqTime','run','wait','submit','start','end']
        for field in fields:
            fields_str += field
            fields_str += sep_sign
        self.job_result.log_print(fields_str[:-1],1)
        i = 0
        done_list = job_module.done_list()
        if len(done_list) <= 100:
            print 'done_list',done_list
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
            context += str(temp_job['reqRan'])
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
            self.job_result.log_print(context,1)
            
            i += 1
        self.job_result.file_close()