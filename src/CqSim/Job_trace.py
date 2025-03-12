from datetime import datetime
from functools import cmp_to_key 
import time
import re
import os

__metaclass__ = type

class Job_trace:
    """
    - Receive formatted job trace file name or the formatted job trace data. 
    - Read the temp file and store the data into a list.
    - Provide all the job trace operations, and keep tracing the information of every job.
    """
    def __init__(
            self,
            job_file_path,
            debug,
            real_start_time = -1,
            virtual_start_time = 0.0, 
            density=1.0, 
            mask = None,
            max_lines = 8000,
            job_runtime_scale_factor = 1.0,
            job_walltime_scale_factor = 1.0):
        """Initialize the Job Trace Module.

        Args:
            job_file_path: Path of the job file to read from.
            real_start_time: Real start time for the simulator.
            virutual_start_time: Virtual start time for the simulator.
            density: The scale of the interval between each job.
            debug: The debug module
            mask: Mask for the job trace
            max_lines: The maximum number of lines to read from job file.
            job_runtime_scaler: Factor to scale the job runtimes by.
            job_walltime_scaler: Factor to scale the job walltimes by.

        Attributes:
            myInfo: Module information.
            real_start_time: Real start time of the trace.
            virtual_start_time: Virutal start time for the simulator.
            density: The scale of the interval between each job.
            debug: The debug module.
            mask: A binary mask for excluding or including jobs.
            max_lines: The maximum number of lines to read from job file.
            cluster_speed: The speed of the cluster.
            jobTrace: Dictionary to keep track of the jobs while simulation.
            job_file_path: The CSV file to read the job submit events from.
            job_fd: file descriptior for the job file read at job_file_path.
            job_counter: counter for the jobs read, also used to assign internal ids.
            job_wait_size: ???
            job_submit_list: ???
            job_wait_list: ???
            job_run_list: ???
            line_number: The line number in the job file.
            job_counter: Counter for the jobs read.
            num_delete_jobs: ???
            job_skips: Counter for the number of jobs skipped (likely because mask was set to 0)
            job_file_offset: offset in number of bytes in the job file for the next job.
        """

        self.myInfo = "Job Trace"
        self.real_start_time = real_start_time
        self.virtual_start_time = virtual_start_time
        self.density = density
        self.debug = debug
        self.mask = mask
        self.max_lines = max_lines
        self.job_runtime_scale_factor = job_runtime_scale_factor
        self.job_walltime_scale_factor = job_walltime_scale_factor
        self.jobTrace={}
        self.job_file_path = job_file_path
        self.job_fd =  open(self.job_file_path,'r')
        self.job_wait_size = 0
        self.job_submit_list=[]
        self.job_wait_list=[]
        self.job_run_list=[]
        self.line_number = 0
        self.job_counter = 0
        self.num_delete_jobs = 0
        self.job_skips = 0
        self.job_file_offest = 0


        # If the mask is not defnied, initialze the mask to read all jobs.
        if self.mask == None:
            self.mask = [1 for _ in range(0, max_lines)]
        
        # If the mask is larger than max lines, truncate it.
        if len(self.mask) > self.max_lines:
            self.mask = self.mask[:self.max_lines]

    def update_max_lines(self, max_lines, default_bit = 1):
        self.max_lines = max_lines

        # If the mask is larger than max_lines, truncate it.
        if len(self.mask) > self.max_lines:
            self.mask = self.mask[:self.max_lines]

        # If the mask is smaller than max_lines, expand the mask.
        if len(self.mask) < self.max_lines:
            difference = self.max_lines - len(self.mask)
            for i in range(difference):
                self.mask.append(default_bit)

    def disable_job(self, line_counter):
        if self.line_number < len(self.mask):
            self.mask[line_counter] = 0
    
    def enable_job(self, line_counter):
        if self.line_number < len(self.mask):
            self.mask[line_counter] = 1 

    def read_next_job(self,):
        """
        Reads the next job in the job file, at the offset kept by the class.

        Args:
        Returns:
            str: String of job data
        """
        line = ""
        with open(self.job_file_path, 'r') as f:
            f.seek(self.job_file_offest)
            line = f.readline()
            self.job_file_offest = f.tell()
        return line



    def dynamic_read_job_file(self):
        """
        Reads the next line from the job file, skips lines accroding to the mask.
        The line is parsed for job data and added to the job trace.
        """
        job_line = self.read_next_job()

        # Check for end of file.
        if not job_line:
            self.job_fd.close()
            return -1
        
        # Check for line number exceeding mask size.
        if self.line_number >= len(self.mask):
            return -1

        # Skip the line if the mask is 0, yield again in parent on -2
        if self.mask[self.line_number] == 0:
            self.line_number += 1
            self.job_skips += 1
            return -2
            

        regex_str = "([^;\\n]*)[;\\n]"
        job_data = re.findall(regex_str, job_line)
        job_data = job_line.split(';')

        
        # If the real start time is not given, use the submit time of the first job.
        if self.real_start_time == -1:
            # Store the submit time of the first job.
            if self.line_number == 0:
                self.real_start_time = float(job_data[1])
        job_info = {'id':int(job_data[0]),\
                    'submit':self.density*(float(job_data[1])-self.real_start_time) + self.virtual_start_time,\
                    'wait':float(job_data[2]),\
                    'run':float(job_data[3]),\
                    'usedProc':int(job_data[4]),\
                    'usedAveCPU':float(job_data[5]),\
                    'usedMem':float(job_data[6]),\
                    'reqProc':int(job_data[7]),\
                    'reqTime':float(job_data[8]),\
                    'reqMem':float(job_data[9]),\
                    'status':int(job_data[10]),\
                    'userID':int(job_data[11]),\
                    'groupID':int(job_data[12]),\
                    'num_exe':int(job_data[13]),\
                    'num_queue':int(job_data[14]),\
                    'num_part':int(job_data[15]),\
                    'num_pre':int(job_data[16]),\
                    'thinkTime':int(job_data[17]),\
                    'start':-1,\
                    'end':-1,\
                    'score':0,\
                    'state':0,\
                    'happy':-1,\
                    'estStart':-1
                }
        
        # Adjust the runtime and walltime according to the scaling factors.
        job_info['run'] = job_info['run'] * self.job_runtime_scale_factor
        job_info['reqTime'] = job_info['reqTime'] * self.job_walltime_scale_factor


        # with open('job_module_log.txt', 'a') as f:
        #     f.write('Scale factor runtime' + str(self.job_runtime_scale_factor) + '\n')
        #     f.write('Scale factor walltime' + str(self.job_walltime_scale_factor) + '\n')
        #     f.write(str(job_info) + '\n\n')

        self.jobTrace[self.job_counter] = job_info
        self.job_submit_list.append(self.job_counter)


        self.line_number += 1
        self.job_counter += 1
        return 0


    def dyn_import_job_file(self):
        """
        [DEPRECATED]
        Old dynamic job file import.
        """

        # Check if the job file is closed
        if self.jobFile.closed:
            return -1
        
        # Something regarding the read input frequency?
        temp_n = 0

        # To read each line of the job file
        regex_str = "([^;\\n]*)[;\\n]"


        while (self.i<self.read_num or self.read_num<=0) and temp_n<self.read_input_freq:
            tempStr = self.jobFile.readline()
            if self.i==self.read_num-1 or not tempStr :    # break when no more line
                self.jobFile.close()
                return -1
                #break
            if (self.j>=self.anchor):
                temp_dataList=re.findall(regex_str,tempStr)

                if self.start == -1:
                    if (self.min_sub<0):
                        self.min_sub=float(temp_dataList[1])
                        if (self.temp_start < 0):
                            self.temp_start = self.min_sub
                        self.start_offset_B = self.min_sub-self.temp_start
                        
                tempInfo = {'id':int(temp_dataList[0]),\
                            'submit':self.density*(float(temp_dataList[1])-self.start),\
                            'wait':float(temp_dataList[2]),\
                            'run':float(temp_dataList[3]),\
                            'usedProc':int(temp_dataList[4]),\
                            'usedAveCPU':float(temp_dataList[5]),\
                            'usedMem':float(temp_dataList[6]),\
                            'reqProc':int(temp_dataList[7]),\
                            'reqTime':float(temp_dataList[8]),\
                            'reqMem':float(temp_dataList[9]),\
                            'status':int(temp_dataList[10]),\
                            'userID':int(temp_dataList[11]),\
                            'groupID':int(temp_dataList[12]),\
                            'num_exe':int(temp_dataList[13]),\
                            'num_queue':int(temp_dataList[14]),\
                            'num_part':int(temp_dataList[15]),\
                            'num_pre':int(temp_dataList[16]),\
                            'thinkTime':int(temp_dataList[17]),\
                            'start':-1,\
                            'end':-1,\
                            'score':0,\
                            'state':0,\
                            'happy':-1,\
                            'estStart':-1}
                #self.jobTrace.append(tempInfo)
                self.jobTrace[self.i] = tempInfo
                self.job_submit_list.append(self.i)
                self.debug.debug(temp_dataList,4)
                #self.debug.debug("* "+str(tempInfo),4)
                self.i += 1      
            self.j += 1
            temp_n += 1
            return 0
    
    def import_job_config (self, config_file):
        #self.debug.debug("* "+self.myInfo+" -- import_job_config",5)
        regex_str = "([^=\\n]*)[=\\n]"
        jobFile = open(config_file,'r')
        config_data={}
                
        self.debug.line(4)
        while (1):
            tempStr = jobFile.readline()
            if not tempStr :    # break when no more line
                break
            temp_dataList=re.findall(regex_str,tempStr)
            config_data[temp_dataList[0]]=temp_dataList[1]
            self.debug.debug(str(temp_dataList[0])+": "+str(temp_dataList[1]),4)
        self.debug.line(4)
        jobFile.close()
        self.start_offset_A = config_data['start_offset']
        self.start_date = config_data['date']
    
    def submit_list (self):
        #self.debug.debug("* "+self.myInfo+" -- submit_list",6)
        return self.job_submit_list
    
    def wait_list (self):
        #self.debug.debug("* "+self.myInfo+" -- wait_list",6)
        return self.job_wait_list
    
    def run_list (self):
        #self.debug.debug("* "+self.myInfo+" -- run_list",6)
        return self.job_run_list
    
    '''
    def done_list (self):
        #self.debug.debug("* "+self.myInfo+" -- done_list",6)
        return self.job_done_list
    '''
    
    def wait_size (self):
        #self.debug.debug("* "+self.myInfo+" -- wait_size",6)
        return self.job_wait_size
    
    def refresh_score (self, score, job_index=None):
        #self.debug.debug("* "+self.myInfo+" -- refresh_score",5)
        if job_index:
            self.jobTrace[job_index]['score'] = score
        else:
            i = 0
            while (i < len(self.job_wait_list)):
                self.jobTrace[self.job_wait_list[i]]['score'] = score[i]
                i += 1
        #self.job_wait_list.sort(self.scoreCmp)
        # python 2 -> 3
        self.job_wait_list.sort(key = cmp_to_key(self.scoreCmp))
        #self.debug.debug("  Wait:"+str(self.job_wait_list),4)

    def scoreCmp(self,jobIndex_c1,jobIndex_c2):
        return -self.cmp(self.jobTrace[jobIndex_c1]['score'],self.jobTrace[jobIndex_c2]['score'])

    def cmp(self, v1, v2):                   # emulate cmp from Python 2
        if (v1 < v2):
            return -1
        elif (v1 == v2):
            return 0
        elif (v1 > v2):
            return 1

    def job_info (self, job_index = -1):
        #self.debug.debug("* "+self.myInfo+" -- job_info",6)
        if job_index == -1:
            return self.jobTrace
        return self.jobTrace[job_index]

    def job_info_len(self):
        return len(self.jobTrace)+self.num_delete_jobs
    
    def job_submit (self, job_index, job_score = 0, job_est_start = -1):
        #self.debug.debug("* "+self.myInfo+" -- job_submit",5)
        self.jobTrace[job_index]["state"]=1
        self.jobTrace[job_index]["score"]=job_score
        self.jobTrace[job_index]["estStart"]=job_est_start
        self.job_submit_list.remove(job_index)
        self.job_wait_list.append(job_index)
        self.job_wait_size += self.jobTrace[job_index]["reqProc"]
        return 1
    
    def job_start (self, job_index, time):
        #self.debug.debug("* "+self.myInfo+" -- job_start",5)
        self.debug.debug(" "+"["+str(job_index)+"]"+" Req:"+str(self.jobTrace[job_index]['reqProc'])+" Run:"+str(self.jobTrace[job_index]['run'])+" ",4)
        self.jobTrace[job_index]["state"]=2
        self.jobTrace[job_index]['start']=time
        self.jobTrace[job_index]['wait']=time-self.jobTrace[job_index]['submit']
        self.jobTrace[job_index]['end'] = time+self.jobTrace[job_index]['run']
        self.job_wait_list.remove(job_index)
        self.job_run_list.append(job_index)
        self.job_wait_size -= self.jobTrace[job_index]["reqProc"]
        return 1
    
    def job_finish (self, job_index, time=None):
        #self.debug.debug("* "+self.myInfo+" -- job_finish",5)
        self.debug.debug(" "+"["+str(job_index)+"]"+" Req:"+str(self.jobTrace[job_index]['reqProc'])+" Run:"+str(self.jobTrace[job_index]['run'])+" ",4)
        self.jobTrace[job_index]["state"]=3
        if  time:
            self.jobTrace[job_index]['end'] = time
        self.job_run_list.remove(job_index)
        #self.job_done_list.append(job_index)
        return 1
    
    '''
    def job_fail (self, job_index, time=None):
        #self.debug.debug("* "+self.myInfo+" -- job_fail",5)
        self.debug.debug(" "+"["+str(job_index)+"]"+" Req:"+str(self.jobTrace[job_index]['reqProc'])+" Run:"+str(self.jobTrace[job_index]['run'])+" ",4)
        self.jobTrace[job_index]["state"]=4
        if  time:
            self.jobTrace[job_index]['end'] = time
        self.job_run_list.remove(job_index)
        self.fail_list.append(job_index)
        return 1
    '''
    
    def job_set_score (self, job_index, job_score):
        #self.debug.debug("* "+self.myInfo+" -- job_set_score",5)
        self.jobTrace[job_index]["score"]=job_score
        return 1

    def remove_job_from_dict(self, job_index):
        del self.jobTrace[job_index]
        self.num_delete_jobs += 1
        #print('jobTrace.keys',self.jobTrace.keys())

    def close_file_job_file(self):
        self.job_fd.close()
    
    
    
    
    
    
    
    
    
