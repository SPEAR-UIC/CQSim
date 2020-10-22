import IOModule.Log_print as Log_print
import copy
import random
import os
from collections import defaultdict

import numpy as np
import time
import logging,copy,os,sys
from collections import Counter
import tensorflow as tf
#import matplotlib.pyplot as plt
#import IPython.display as ipydis
# turn off all the deprecation warnings
tf.logging.set_verbosity(logging.ERROR)
# turn on eager execution
tf.enable_eager_execution()
tfe = tf.contrib.eager
print('Tensorflow Version: %s',tf.__version__)

__metaclass__ = type

class Cqsim_sim:
    def __init__(self, module, debug = None, monitor = None, backfill_flag = 1, epsilon=0.25, epsilon_decay=0.9995,epsilon_min=0.001,training_size=10, lamda=0.7, discount_span=3600, weight_fn = None, reward_type='1',sleep='0',use_window='0',is_training='0', GAMMA=0.99):
        self.myInfo = "Cqsim Sim"
        self.module = module
        self.debug = debug
        self.monitor = monitor
        self.backfill_flag = int(backfill_flag)
        self.sleep = sleep
        self.use_window=int(use_window)
        
        
        self.debug.line(4," ")
        self.debug.line(4,"#")
        self.debug.debug("# "+self.myInfo,1)
        self.debug.line(4,"#")
        
        self.event_seq = []
        #self.event_pointer = 0
        self.monitor_start = 0
        self.current_event = None
        #obsolete
        self.job_num = len(self.module['job'].job_info())
        self.currentTime = 0
        #obsolete
        self.read_job_buf_size = 100
        self.read_job_pointer = 0 # next position in job list
        self.previous_read_job_time = -1 # lastest read job submit time

        # learning parameters
        self.is_training=int(is_training)
        self.epsilon = float(epsilon)
        self.epsilon_decay = float(epsilon_decay)
        self.epsilon_min = float(epsilon_min)
        self.lamda = float(lamda)
        self.grads_seq = []
        self.value_seq = []
        self.reward_seq = []
        self.job_start_time_seq = []
        self.batch_delta = []
        self.uti_dict = defaultdict(float)
        self.reward_dict = defaultdict(float)
        self.wait_times_dict = defaultdict(list)
        self.uti_batch_dict = defaultdict(float)
        self.training_size = int(training_size)
        self.training_cnt = 0
        self.discount_span=float(discount_span)
        self.weight_fn = weight_fn
        # reward_type: 1. utilization, 2.wait_time, 3.utilization+wait_time
        self.reward_type = reward_type
        self.job_immediate_reward_seq = []
        self.gamma = float(lamda)
        
        self.debug.line(4)
        for module_name in self.module:
            temp_name = self.module[module_name].myInfo
            self.debug.debug(temp_name+" ................... Load",4)
            self.debug.line(4)
        
    def reset(self, module = None, debug = None, monitor = None, backfill_flag = 1, epsilon=0.25, epsilon_decay=0.9995, epsilon_min=0.001,training_size=10, lamda=0.7, discount_span=3600, weight_fn = None, reward_type='1',sleep='0',use_window='0',is_training='0', GAMMA=0.99):
        #self.debug.debug("# "+self.myInfo+" -- reset",5)
        if module:
            self.module = module
        
        if debug:
            self.debug = debug
        if monitor:
            self.monitor = monitor

        self.backfill_flag = int(backfill_flag)
        self.sleep = sleep
        self.use_window=int(use_window)
               
            
        self.event_seq = []
        #self.event_pointer = 0
        self.monitor_start = 0
        self.current_event = None
        #obsolete
        self.job_num = len(self.module['job'].job_info())
        self.currentTime = 0
        #obsolete
        self.read_job_buf_size = 100
        self.read_job_pointer = 0
        self.previous_read_job_time = -1
        # learning parameters
        self.is_training=int(is_training)
        self.epsilon = float(epsilon)
        self.epsilon_decay = float(epsilon_decay)
        self.epsilon_min = float(epsilon_min)
        self.lamda = float(lamda)
        self.grads_seq = []
        self.value_seq = []
        self.reward_seq = []
        self.job_start_time_seq = []
        self.batch_delta = []
        self.uti_dict = defaultdict(float)
        self.reward_dict = defaultdict(float)
        self.wait_times_dict = defaultdict(list)
        self.uti_batch_dict = defaultdict(float)
        self.training_size = int(training_size)
        self.training_cnt = 0
        self.discount_span=float(discount_span)
        self.weight_fn = weight_fn
        self.reward_type = reward_type
        self.job_immediate_reward_seq = []
        self.gamma = float(lamda)

        
    def cqsim_sim(self):
        #self.debug.debug("# "+self.myInfo+" -- cqsim_sim",5)
        #self.insert_submit_events()

        lastest_num = 0
        if self.weight_fn:
            checkpoint_folder, checkpoint_files_start_with = self.weight_fn.rsplit('/', 1)
            for file in os.listdir(checkpoint_folder):  
                if file.startswith(checkpoint_files_start_with):    
                    file_str = file.replace(checkpoint_files_start_with,"").rsplit('.',1)[0].rsplit('_',1)[-1]  
                    if file_str.isdigit():  
                        file_num = int(file_str)    
                        lastest_num = max(lastest_num, file_num)    
            checkpoint_filename = self.weight_fn+"_"+str(lastest_num)+".h5"


        if self.weight_fn and os.path.exists(checkpoint_filename):
            self.module['learning'].load_weights(checkpoint_filename)
            print('................... Loading weights from '+checkpoint_filename)
            self.epsilon = 1.0
            if self.is_training==0:
                self.epsilon = 1
        else:
        	self.debug.debug("................... Does not have saved weights to load.")

        self.import_submit_events()
        #self.insert_event_job()
        self.insert_event_extend()
        self.scan_event()

        if self.is_training!=0 and self.weight_fn:
            self.module['learning'].save_weights(self.weight_fn+"_"+str(lastest_num+1)+".h5")
            self.debug.debug("................... save weights to "+self.weight_fn,2)
        else:
        	self.debug.debug("................... Did not save weights.")

        self.print_result()
        self.debug.debug("------ Simulating Done!",2) 
        self.debug.debug(lvl=1) 
        if self.sleep != '0':
            os.system("pmset sleepnow")
        return

    def import_submit_events(self):
        # fread jobs to job list and buffer to event_list dynamically
        if self.read_job_pointer < 0:
            return -1
        temp_return = self.module['job'].dyn_import_job_file()

        i = self.read_job_pointer
        #while (i < len(self.module['job'].job_info())):
        while (i < self.module['job'].job_info_len()):
            self.insert_event(1,self.module['job'].job_info(i)['submit'],2,[1,i])
            self.previous_read_job_time = self.module['job'].job_info(i)['submit']
            self.debug.debug("  "+"Insert job["+"2"+"] "+str(self.module['job'].job_info(i)['submit']),4)
            i += 1
        #print("Insert Jobs!")
        if temp_return == None or temp_return < 0 :
            self.read_job_pointer = -1
            return -1
        else:
            self.read_job_pointer = i
            return 0

    #obsolete
    def insert_submit_events(self):
        # first read all jobs to job list, buffer to event_list dynamically
        #self.debug.debug("# "+self.myInfo+" -- insert_event_job",5) 
        if self.read_job_pointer < 0:
            return -1
        i = self.read_job_pointer
        while (i < self.read_job_buf_size + self.read_job_pointer and i < self.job_num):
            self.insert_event(1,self.module['job'].job_info(i)['submit'],2,[1,i])
            self.previous_read_job_time = self.module['job'].job_info(i)['submit']
            self.debug.debug("  "+"Insert job["+"2"+"] "+str(self.module['job'].job_info(i)['submit']),4)
            i += 1
        if i >= self.job_num:
            self.read_job_pointer = -1
        else:
            self.read_job_pointer = i
        return 0
    
    #obsolete
    def insert_event_job(self):
        #self.debug.debug("# "+self.myInfo+" -- insert_event_job",5) 
        i = 0
        while (i < self.job_num):
            self.insert_event(1,self.module['job'].job_info(i)['submit'],2,[1,i])
            self.debug.debug("  "+"Insert job["+"2"+"] "+str(self.module['job'].job_info(i)['submit']),4)
            i += 1
        return
    
    def insert_event_monitor(self, start, end):
        #self.debug.debug("# "+self.myInfo+" -- insert_event_monitor",5) 
        if (not self.monitor):
            return -1
        temp_num = start/self.monitor
        temp_num = int(temp_num)
        temp_time = temp_num*self.monitor

        #self.monitor_start=self.event_pointer
        self.monitor_start=0

        i = 0
        while (temp_time < end):
            if (temp_time>=start):
                self.insert_event(2,temp_time,5,None)
                self.debug.debug("  "+"Insert mon["+"5"+"] "+str(temp_time),4)
            temp_time += self.monitor
        return
    
    def insert_event_extend(self):
        #self.debug.debug("# "+self.myInfo+" -- insert_event_extend",5) 
        return
    
    def insert_event(self, type, time, priority, para = None):
        #self.debug.debug("# "+self.myInfo+" -- insert_event",5) 
        temp_index = -1
        new_event = {"type":type, "time":time, "prio":priority, "para":para}
        if (type == 1):
            #i = self.event_pointer
            i = 0
            while (i<len(self.event_seq)):
                if (self.event_seq[i]['time']==time):
                    if (self.event_seq[i]['prio']>priority):
                        temp_index = i
                        break
                elif (self.event_seq[i]['time']>time):
                    temp_index = i
                    break 
                i += 1
        elif (type == 2):
            temp_index = self.get_index_monitor()
            
        if (temp_index>=len(self.event_seq) or temp_index == -1):
            self.event_seq.append(new_event)
        else:
            self.event_seq.insert(temp_index,new_event)
            
    
    def delete_event(self, type, time, index):
        #self.debug.debug("# "+self.myInfo+" -- delete_event",5) 
        return
    
    def get_index_monitor (self):
        #self.debug.debug("# "+self.myInfo+" -- get_index_monitor",5) 
        '''
        if (self.event_pointer>=self.monitor_start):
            self.monitor_start=self.event_pointer+1
        temp_mon = self.monitor_start
        self.monitor_start += 1
        return temp_mon
        '''
        self.monitor_start += 1
        return self.monitor_start

    
    def scan_event(self):
       # self.debug.debug("# "+self.myInfo+" -- scan_event",5) 
        self.debug.line(2," ")
        self.debug.line(2,"=")
        self.debug.line(2,"=")
        self.current_event = None
        #while (self.event_pointer < len(self.event_seq) or self.read_job_pointer >= 0):
        while (len(self.event_seq) > 0 or self.read_job_pointer >= 0):
            #print('event_seq',len(self.event_seq))
            if len(self.event_seq) > 0:
                temp_current_event = self.event_seq[0]
                temp_currentTime = temp_current_event['time']
            else:
                temp_current_event = None
                temp_currentTime = -1
            #if (temp_currentTime >= self.previous_read_job_time or self.event_pointer >= len(self.event_seq)) and self.read_job_pointer >= 0:
            if (len(self.event_seq) == 0 or temp_currentTime >= self.previous_read_job_time) and self.read_job_pointer >= 0:
                #print('insert_submit_events from scan_event',temp_currentTime >= self.previous_read_job_time,(self.event_pointer >= len(self.event_seq) and self.read_job_pointer >= 0))
                #self.insert_submit_events()
                self.import_submit_events()
                continue
            self.current_event = temp_current_event
            self.currentTime = temp_currentTime
            if (self.current_event['type'] == 1):
                self.debug.line(2," ") 
                self.debug.line(2,">>>") 
                self.debug.line(2,"--") 
                #print ("  Time: "+str(self.currentTime)) 
                self.debug.debug("  Time: "+str(self.currentTime),2) 
                self.debug.debug("   "+str(self.current_event),2)
                self.debug.line(2,"--") 
                self.debug.debug("  Wait: "+str(self.module['job'].wait_list()),2) 
                self.debug.debug("  Run : "+str(self.module['job'].run_list()),2) 
                self.debug.line(2,"--") 
                self.debug.debug("  Tot:"+str(self.module['node'].get_tot())+" Idle:"+str(self.module['node'].get_idle())+" Avail:"+str(self.module['node'].get_avail())+" ",2)
                self.debug.line(2,"--") 
                
                self.event_job(self.current_event['para'])
            elif (self.current_event['type'] == 2):
                self.event_monitor(self.current_event['para'])
            elif (self.current_event['type'] == 3):
                self.event_extend(self.current_event['para'])
            self.sys_collect()
            self.interface()
            #self.event_pointer += 1
            del self.event_seq[0]
        self.debug.line(2,"=")
        self.debug.line(2,"=")
        self.debug.line(2," ")
        return
    
    def event_job(self, para_in = None):
        #self.debug.debug("# "+self.myInfo+" -- event_job",5) 
        '''
        self.debug.line(2,"xxxxx")
        i = 0
        while (i<len(self.event_seq)):
            self.debug.debug(self.event_seq[i],2) 
            i += 1
            
        self.debug.line(2,"xxxxx")
        self.debug.line(2," ")
        self.debug.line(2," ")
        '''
        if (self.current_event['para'][0] == 1):
            self.submit(self.current_event['para'][1])
        elif (self.current_event['para'][0] == 2):
            self.finish(self.current_event['para'][1])
        #self.score_calculate()
        self.start_scan()
        #if (self.event_pointer < len(self.event_seq)-1):
        if (len(self.event_seq) > 1):
            #self.insert_event_monitor(self.currentTime, self.event_seq[self.event_pointer+1]['time'])
            self.insert_event_monitor(self.currentTime, self.event_seq[1]['time'])
        return
    
    def event_monitor(self, para_in = None):
        #self.debug.debug("# "+self.myInfo+" -- event_monitor",5) 
        self.alg_adapt()
        self.window_adapt()
        self.print_adapt(None)
        return
    
    def event_extend(self, para_in = None):
        #self.debug.debug("# "+self.myInfo+" -- event_extend",5) 
        return
    
    def submit(self, job_index):
        #self.debug.debug("# "+self.myInfo+" -- submit",5) 
        self.debug.debug("[Submit]  "+str(job_index),3)
        self.module['job'].job_submit(job_index)
        return
    
    def finish(self, job_index):
        #self.debug.debug("# "+self.myInfo+" -- finish",5) 
        self.debug.debug("[Finish]  "+str(job_index),3)
        self.module['node'].node_release(job_index,self.currentTime)
        self.module['job'].job_finish(job_index)
        self.module['output'].print_result(self.module['job'], job_index)
        self.module['job'].remove_job_from_dict(job_index)
        return
    
    def start(self, job_index):
        #self.debug.debug("# "+self.myInfo+" -- start",5) 
        self.debug.debug("[Start]  "+str(job_index),3)
        self.debug.debug('Job '+str(job_index)+" starting <<< " + str(self.module['job'].job_info(job_index)['reqProc']),4)
        self.module['node'].node_allocate(self.module['job'].job_info(job_index)['reqProc'], job_index,\
         self.currentTime, self.currentTime + self.module['job'].job_info(job_index)['reqTime'])
        self.module['job'].job_start(job_index, self.currentTime)
        self.insert_event(1,self.currentTime+self.module['job'].job_info(job_index)['run'],1,[2,job_index])
        return
    
    def score_calculate(self):
        #self.debug.debug("# "+self.myInfo+" -- score_calculate",5) 
        temp_wait_list = self.module['job'].wait_list()
        wait_num = len(temp_wait_list)
        temp_wait=[]
        i = 0
        while (i<wait_num):
            temp_job = self.module['job'].job_info(temp_wait_list[i])
            temp_wait.append(temp_job)
            i += 1
        score_list = self.module['alg'].get_score(temp_wait,self.currentTime)
        self.module['job'].refresh_score(score_list)
        return 

    def score_calculate(self, wait_jobs):
        #self.debug.debug("# "+self.myInfo+" -- score_calculate",5) 
        temp_wait_list = wait_jobs
        wait_num = len(temp_wait_list)
        temp_wait=[]
        idx_list = []
        available_nodes = self.module['node'].get_avail()
        max_wait_time = 0
        window_size = self.module['learning'].window_size
        if self.use_window==0:
        	window_size = float('Inf')
        i = 0
        while (i<wait_num):
            if i<window_size:
                temp_job = self.module['job'].job_info(temp_wait_list[i])
                #if temp_job['reqProc'] <= available_nodes:
                temp_wait.append(temp_job)
                #idx_list.append(i) #?
            max_wait_time = max(max_wait_time, self.currentTime-temp_job['submit']) # all jobs or eligible jobs ?
            i += 1

        if not temp_wait:
            return -1, None, max_wait_time

        temp_nodeStruc = self.module['node'].get_nodeStruc()
        time1 = time.time()
        max_idx, selected_fv = self.module['alg'].compute_score(temp_wait, temp_nodeStruc, self.currentTime, epsilon = self.epsilon)
        self.debug.debug('Normal Job Selction Time: '+str(time.time()-time1), 3)
        #self.module['job'].refresh_score(score_list)
        #print('idx_list',idx_list)
        #print('temp_wait',len(temp_wait))
        #print('max_idx',max_idx,idx_list[max_idx])
        #return idx_list[max_idx], selected_fv, max_wait_time
        return max_idx, selected_fv, max_wait_time

    def update_job_order(self, wait_jobs):
        max_idx, selected_fv, max_job_wait_time = self.score_calculate(wait_jobs)
        #print(wait_jobs,score_list)
        #max_idx = score_list.index(max(score_list)) 
        if max_idx>0:
            temp_wait_jobs = [wait_jobs[max_idx]] + wait_jobs[:max_idx] + wait_jobs[max_idx+1:]
            return temp_wait_jobs, selected_fv, max_job_wait_time
        else:
            return wait_jobs, selected_fv, max_job_wait_time

    def get_reward(self, job_info, max_job_wait_time):
        
        if self.reward_type == '2':
            selected_job_wait_time = self.currentTime-job_info['submit']
            wait_times_ratio = 1
            if max_job_wait_time>0:
                wait_times_ratio = selected_job_wait_time/max_job_wait_time
            reward = wait_times_ratio
            self.wait_times_dict[self.currentTime].append(reward)
            self.reward_dict[self.currentTime] = sum(self.wait_times_dict[self.currentTime])/len(self.wait_times_dict[self.currentTime])
            #print('reward: wait_times_ratio',reward)
        elif self.reward_type == '3':
            tot = self.module['node'].get_tot()
            idle = self.module['node'].get_idle()
            uti = float(tot-idle)/tot
            self.uti_dict[self.currentTime] = max(self.uti_dict[self.currentTime], uti)

            selected_job_wait_time = self.currentTime-job_info['submit']
            wait_times_ratio = 1
            if max_job_wait_time>0:
                wait_times_ratio = selected_job_wait_time/max_job_wait_time
            #reward = (uti+wait_times_ratio)/2
            self.wait_times_dict[self.currentTime].append(wait_times_ratio)
            cur_average_wait_time_ratio = sum(self.wait_times_dict[self.currentTime])/len(self.wait_times_dict[self.currentTime]) # average or minimimal ?
            self.reward_dict[self.currentTime] = (max(self.uti_dict[self.currentTime], uti)+cur_average_wait_time_ratio)/2
            #print('reward:(uti+wait_times_ratio)/2',reward)
        elif self.reward_type == '4':
            # uti+award
            priority_weigth = 1.25
            wait_times_ratio = 1
            selected_job_wait_time = self.currentTime-job_info['submit']
            if max_job_wait_time>0:
                wait_times_ratio = selected_job_wait_time/max_job_wait_time
            if max_job_wait_time>60*60*24*10 and wait_times_ratio<0.75:
                wait_times_ratio = 0.1
            else:
                wait_times_ratio = 1

            tot = self.module['node'].get_tot()
            if self.currentTime in self.uti_dict:
                if job_info['award'] == 1:
                    uti = self.uti_dict[self.currentTime]+float(job_info['reqProc']*priority_weigth*wait_times_ratio)/tot
                else:
                    uti = self.uti_dict[self.currentTime]+float(job_info['reqProc']*wait_times_ratio)/tot
            else:
                idle = self.module['node'].get_idle()
                uti = float(tot-idle)/tot
                #print('job_info[award]',job_info)
                if job_info['award'] == 1:
                    uti += float((priority_weigth-1)*job_info['reqProc'])/tot
                uti *= wait_times_ratio
            self.uti_dict[self.currentTime] = max(self.uti_dict[self.currentTime], uti)
            self.reward_dict[self.currentTime] = self.uti_dict[self.currentTime]
        elif self.reward_type == '5':
            #self.job_immediate_reward_seq.append(job_info['reqProc'])
            tmp_reward = 0

            tot = self.module['node'].get_tot()
            idle = self.module['node'].get_idle()
            running = tot-idle
            selected_job_requested_nodes = job_info['reqProc']
            selected_job_wait_time = self.currentTime-job_info['submit']

            #selected_job_priority = 1 if selected_job_requested_nodes>=802 else 0
            selected_job_priority = selected_job_requested_nodes/tot
            w1, w2, w3 = 1/3, 1/3, 1/3

            if idle<selected_job_requested_nodes:   
                tmp_reward += running/tot*w1    
            else:   
                tmp_reward += (selected_job_requested_nodes+running)/tot*w1 
            # 6 hours 60%   
            if max_job_wait_time>=21600:    
                tmp_reward += selected_job_wait_time/max_job_wait_time*w2   
            else:   
                tmp_reward += selected_job_wait_time/21600*w2   
            tmp_reward += selected_job_priority*w3  
                
            self.job_immediate_reward_seq.append(tmp_reward)    
            self.module['output'].print_reward_info(tmp_reward)
        elif self.reward_type == '6':
            tot = self.module['node'].get_tot()
            self.job_immediate_reward_seq.append(float(job_info['reqProc'])/tot)
            #self.job_immediate_reward_seq.append(float(job_info['reqProc']))
        else:
            # uti
            tot = self.module['node'].get_tot()
            idle = self.module['node'].get_idle()
            uti = float(tot-idle)/tot
            self.uti_dict[self.currentTime] = max(self.uti_dict[self.currentTime], uti)
            self.reward_dict[self.currentTime] = self.uti_dict[self.currentTime]
            #print('reward: uti',reward)

        #print('selected_job_wait_time',selected_job_wait_time, 'max_job_wait_time',max_job_wait_time,'wait_times_ratio',wait_times_ratio)
        #print('time',self.currentTime,'uti',uti,self.uti_dict[self.currentTime])

        #self.uti_dict[self.currentTime] = max(self.uti_dict[self.currentTime], reward)
        #print('time',self.currentTime,'uti',uti,self.uti_dict[self.currentTime])
        #print('self.reward_dict',self.reward_dict)

        #return uti # Todo

    def get_no_reward(self):
        self.job_immediate_reward_seq.append(0)

    def get_batch_rewards(self):
        time_seq = sorted(self.reward_dict)
        time_diff = [j-i for i, j in zip(time_seq[:-1],time_seq[1:])]
        uti_list = [self.reward_dict[key] for key in sorted(self.reward_dict)]
        last_uti = uti_list[-1]
        uti_list = uti_list[:-1]
        tu = np.array(time_diff)*np.array(uti_list)
        for i in range(len(tu)-2,-1,-1):
            tu[i] += tu[i+1]
        max_time = time_seq[-1]
        for t,m in zip(time_seq[:-1], tu):
            self.uti_batch_dict[t] = m/(max_time-t)
        self.uti_batch_dict[max_time] = last_uti # 1.0 or last_uti

        for t in self.job_start_time_seq:
            self.reward_seq.append(self.uti_batch_dict[t])

        #print('self.uti_dict',self.uti_dict)
        #print('self.uti_batch_dict',self.uti_batch_dict)
        #print('self.reward_seq',self.reward_seq)

    def get_batch_rewards_span(self):
        time_seq = sorted(self.reward_dict)
        uti_list = [self.reward_dict[key] for key in sorted(self.reward_dict)]
        last_uti = uti_list[-1]
        uti_list = uti_list[:-1]

        for i in range(len(uti_list)):
            end_time = min(time_seq[i]+self.discount_span,time_seq[-1])
            #print(time_seq[i],end_time)
            j = i+1
            tu = 0
            while j<len(time_seq) and time_seq[j-1]<end_time:
                td = min(time_seq[j],end_time)-time_seq[j-1]
                #print('td',td,'uti',uti_list[j-1])
                tu += td*uti_list[j-1]
                j += 1

            self.reward_seq.append(tu/(end_time-time_seq[i]))
            #print('---')
        self.reward_seq.append(last_uti) # 1.0 or last_uti

        #print('self.uti_dict',self.uti_dict)
        #print('self.reward_seq',self.reward_seq)
    
    def start_scan(self):
        #self.debug.debug("# "+self.myInfo+" -- start_scan",5) 
        while True:
            temp_wait = self.module['job'].wait_list()
            wait_num = len(temp_wait)
            if wait_num == 0:
                break
            #print('temp_wait_before',temp_wait)
            temp_wait, selected_fv, max_job_wait_time = self.update_job_order(temp_wait)
            #print('temp_wait_scan',temp_wait)
            temp_job = self.module['job'].job_info(temp_wait[0])
            if (self.module['node'].is_available(temp_job['reqProc'])):

                if self.epsilon>self.epsilon_min:
                    self.epsilon *= self.epsilon_decay
                else:
                    self.epsilon = self.epsilon_min

                self.debug.debug('Normal start job <<<'+ str(temp_wait[0]),4)

                self.start(temp_wait[0])

                if self.is_training==0:
                    continue

                self.get_reward(temp_job, max_job_wait_time)
                value, grads = self.module['agent'].grad(selected_fv)
                value = tf.reshape(value,[-1])
                #print('value', value, 'reward',reward,'grads',len(grads))
                self.value_seq.append(value)
                self.grads_seq.append(grads)
                #self.reward_seq.append(reward)
                self.job_start_time_seq.append(self.currentTime)

            else:
                break

        temp_wait = self.module['job'].wait_list()
        if self.backfill_flag>0 and len(temp_wait) > 1:
            #print('Start backfilling .......')
            self.backfill(temp_wait)

        self.training_cnt += 1

        # batch training
        if self.training_cnt>=self.training_size:
            if len(self.job_immediate_reward_seq)==0:
                return
            start_train_time = time.time()

            #self.get_batch_rewards()
            #self.get_batch_rewards_span()
            G = np.zeros_like(self.job_immediate_reward_seq)
            for t in range(len(self.job_immediate_reward_seq)):
                G_sum = 0
                discount = 1
                for k in range(t, len(self.job_immediate_reward_seq)):
                    G_sum += self.job_immediate_reward_seq[k] * discount
                    discount *= self.gamma
                #self.reward_seq.append(G_sum)

                G[t] = G_sum
            
            mean = np.mean(G)
            std = np.std(G) if np.std(G) > 0 else 1
            max_G = max(G)
            #standard_G = G - mean
            #total_standard_G = sum(standard_G)
            #self.reward_seq = (G - mean) / std
            self.reward_seq = [float(g)/max_G for g in G]
            #self.reward_seq = [float(g)/total_standard_G for g in standard_G]
            

            time1 = time.time()

            #print('Time 1: get_batch_rewards_span', time1-start_train_time)


            #print('_____batch training_____')

            time2 = time.time()
            
            delta_seq = np.array([j - i for i, j in zip(self.reward_seq, self.value_seq)])
            self.debug.debug('self.reward_seq:'+str(self.reward_seq),3)
            print('self.value_seq:',self.value_seq)

            #print('Time 2: delta_seq', time2-time1)


            # loop over the gradients at each move
            accu_grads = None
            accu_t = 0
            #batch_delta = []
            for t, grads in enumerate(self.grads_seq):
              # sum the delta for all future steps, weighted by the lamda raised to the number of moves into the future
              delta_sum = np.sum([(self.lamda ** j) * delta for j, delta in enumerate(delta_seq[t:])])
              #print('self.value_seq',self.value_seq)
              self.debug.debug('delta_sum'+str(delta_sum),3)
              #print(grads)
              new_grads = [-delta_sum * g for g in grads] # grads?
              #print('new_grads',new_grads)
              self.module['agent'].apply_gradients(new_grads)
              #print('new_grads',new_grads)
              #batch_delta.append(new_grads)
              '''
              if not accu_grads:
                #accu_grads = [-delta_sum * g for g in grads]
                accu_grads = [g for g in new_grads]
              else:
                #accu_grads = [-delta_sum*g+a for g,a in zip(grads,accu_grads)]
                accu_grads = [g+a for g,a in zip(new_grads,accu_grads)]
              accu_t = t
              '''

            time3 = time.time()

            #print('Time 3: compute accu_grads', time3-time2)

            #avg_grads = np.mean(batch_delta, axis=0)
            #accu_t += 1
            #avg_grads = np.divide(accu_grads,accu_t)

            #avg_grads = [a/accu_t for a in accu_grads]

            #print('accu_grads',accu_grads)
            #print('avg_grads',avg_grads)

            time4 = time.time()
            #print('Time 4: compute avg_grads', time4-time3)


            
            # apply these gradients
            #self.module['agent'].apply_gradients(avg_grads)
            #print('accu_grads',accu_grads)
            #self.module['agent'].apply_gradients(accu_grads)

            time5 = time.time()
            #print('Time 5: apply_gradients', time5-time4)
            #batch_delta = []

            # reset training parameters
            self.training_cnt = 0
            self.value_seq = []
            self.grads_seq = []
            self.reward_seq = []
            self.job_start_time_seq = []
            self.uti_dict = defaultdict(float)
            self.reward_dict = defaultdict(float)
            self.wait_times_dict = defaultdict(list)
            self.uti_batch_dict = defaultdict(float)
            self.job_immediate_reward_seq = []
            self.debug.debug('Batch Training Time: '+str(time.time()-start_train_time), 3)

        return

        '''
        start_max = self.module['win'].start_num()
        temp_wait = self.module['job'].wait_list()
        wait_num = len(temp_wait)
        win_count = start_max
            
        i = 0
        while (i<wait_num):
            if (win_count >= start_max):
                win_count = 0
                temp_wait = self.start_window(temp_wait)

            
            #print "....  ", temp_wait[i]
            temp_job = self.module['job'].job_info(temp_wait[i])
            if (self.module['node'].is_available(temp_job['reqProc'])):
                self.start(temp_wait[i])
            else:
                temp_wait = self.module['job'].wait_list()
                self.backfill(temp_wait)
                break
            i += 1
            win_count += 1
        return
        '''
    
    def start_window(self, temp_wait_B):
        #self.debug.debug("# "+self.myInfo+" -- start_window",5) 
        win_size = self.module['win'].window_size()
        
        if (len(temp_wait_B)>win_size):
            temp_wait_A = temp_wait_B[0:win_size]
            temp_wait_B = temp_wait_B[win_size:]
        else:
            temp_wait_A = temp_wait_B
            temp_wait_B = []

        temp_wait_info = []
        max_num = len(temp_wait_A)
        i = 0
        while (i < max_num):
            temp_job = self.module['job'].job_info(temp_wait_A[i])
            temp_wait_info.append({"index":temp_wait_A[i],"proc":temp_job['reqProc'],\
             "node":temp_job['reqProc'],"run":temp_job['run'],"score":temp_job['score']})
            i += 1 
            
        temp_wait_A = self.module['win'].start_window(temp_wait_info,{"time":self.currentTime})
        temp_wait_B[0:0] = temp_wait_A
        return temp_wait_B
    
    def backfill(self, temp_wait):
        #self.debug.debug("# "+self.myInfo+" -- backfill",5) 
        temp_wait_info = []
        max_num = len(temp_wait)
        i = 0
        max_wait_time = 0
        while (i < max_num):
            temp_job = self.module['job'].job_info(temp_wait[i])
            max_wait_time = max(max_wait_time, self.currentTime-temp_job['submit'])
            temp_wait_info.append({"index":temp_wait[i],"proc":temp_job['reqProc'],\
             "node":temp_job['reqProc'],"run":temp_job['run'],"score":temp_job['score'],"submit":temp_job['submit'],"reqTime":temp_job['reqTime'],"reqProc":temp_job['reqProc'],"award":temp_job['award']})
            i += 1
        time1 = time.time()
        backfill_list, selected_fv_list = self.module['backfill'].backfill(temp_wait_info, {'time':self.currentTime, 'alg_module':self.module['alg'], 'epsilon': self.epsilon})
        self.debug.debug('Backfilling List Time: '+str(time.time()-time1), 3)
        if backfill_list:
            self.debug.debug('backfill_list ....'+str(backfill_list),4)
        #self.debug.debug("HHHHHHHHHHHHH "+str(backfill_list)+" -- backfill",2) 
        if not backfill_list:
            return 0
        
        if selected_fv_list:
            #print('selected_fv_list',len(selected_fv_list))
            for job, selected_fv in zip(backfill_list, selected_fv_list):
                self.debug.debug('Backfill start job <<<'+str(job),4)
                self.start(job)
                if self.is_training==0:
                    continue
                ### learning processing same as previous ###
                job_info = self.module['job'].job_info(job)
                self.get_reward(job_info, max_wait_time)
                value, grads = self.module['agent'].grad(selected_fv)
                value = tf.reshape(value,[-1])
                #print('value', value, 'reward',reward,'grads',len(grads))
                self.value_seq.append(value)
                self.grads_seq.append(grads)
                #self.reward_seq.append(reward)
                self.job_start_time_seq.append(self.currentTime)

                '''

                self.training_cnt += 1

                # batch training
                if self.training_cnt==self.training_size:
                    start_train_time = time.time()

                    #self.get_batch_rewards()
                    #self.get_batch_rewards_span()
                    for t in range(len(self.job_immediate_reward_seq)):
                        G_sum = 0
                        discount = 1
                        for k in range(t, len(self.job_immediate_reward_seq)):
                            G_sum += self.job_immediate_reward_seq[k] * discount
                            discount *= self.gamma
                        self.reward_seq.append(G_sum)

                    time1 = time.time()

                    #print('Time 1: get_batch_rewards_span', time1-start_train_time)


                    #print('_____batch training_____')

                    time2 = time.time()
                    
                    delta_seq = np.array([j - i for i, j in zip(self.reward_seq, self.value_seq)])

                    #print('Time 2: delta_seq', time2-time1)


                    # loop over the gradients at each move
                    accu_grads = None
                    accu_t = 0
                    #batch_delta = []
                    for t, grads in enumerate(self.grads_seq):
                      # sum the delta for all future steps, weighted by the lamda raised to the number of moves into the future
                      delta_sum = np.sum([(self.lamda ** j) * delta for j, delta in enumerate(delta_seq[t:])])
                      new_grads = [-delta_sum * g for g in grads] # grads?
                      #batch_delta.append(new_grads)
                      if not accu_grads:
                        #accu_grads = [-delta_sum * g for g in grads]
                        accu_grads = [g for g in new_grads]
                      else:
                        #accu_grads = [-delta_sum*g+a for g,a in zip(grads,accu_grads)]
                        accu_grads = [g+a for g,a in zip(new_grads,accu_grads)]
                      accu_t = t

                    time3 = time.time()

                    #print('Time 3: compute accu_grads', time3-time2)

                    #avg_grads = np.mean(batch_delta, axis=0)
                    accu_t += 1
                    #avg_grads = np.divide(accu_grads,accu_t)
                    avg_grads = [a/accu_t for a in accu_grads]

                    #print('accu_grads',accu_grads)
                    #print('avg_grads',avg_grads)

                    time4 = time.time()
                    #print('Time 4: compute avg_grads', time4-time3)


                    
                    # apply these gradients
                    self.module['agent'].apply_gradients(avg_grads)

                    time5 = time.time()
                    #print('Time 5: apply_gradients', time5-time4)
                    #batch_delta = []

                    # reset training parameters
                    self.training_cnt = 0
                    self.value_seq = []
                    self.grads_seq = []
                    self.reward_seq = []
                    self.job_start_time_seq = []
                    self.uti_dict = defaultdict(float)
                    self.reward_dict = defaultdict(float)
                    self.wait_times_dict = defaultdict(list)
                    self.uti_batch_dict = defaultdict(float)
                    self.job_immediate_reward_seq = []
                    #print('Batch Training Time: ', time.time()-start_train_time)
                    self.debug.debug('Batch Training Time: '+str(time.time()-start_train_time), 3)
                '''

                #############################################
        else:
            for job in backfill_list:
                self.debug.debug('Backfill no feature vector start job <<<'+str(job),4)
                self.start(job)
        return 1
    
    def sys_collect(self):
        #self.debug.debug("# "+self.myInfo+" -- sys_collect",5) 
        '''
        temp_inter = 0
        if (self.event_pointer+1<len(self.event_seq)):
            temp_inter = self.event_seq[self.event_pointer+1]['time'] - self.currentTime
        temp_size = 0
        
        event_code=None
        if (self.event_seq[self.event_pointer]['type'] == 1):
            if (self.event_seq[self.event_pointer]['para'][0] == 1):   
                event_code='S'
            elif(self.event_seq[self.event_pointer]['para'][0] == 2):   
                event_code='E'
        elif (self.event_seq[self.event_pointer]['type'] == 2):
            event_code='Q'
        '''
        temp_inter = 0
        if (len(self.event_seq) > 1):
            temp_inter = self.event_seq[1]['time'] - self.currentTime
        temp_size = 0
        
        event_code=None
        if (self.event_seq[0]['type'] == 1):
            if (self.event_seq[0]['para'][0] == 1):   
                event_code='S'
            elif(self.event_seq[0]['para'][0] == 2):   
                event_code='E'
        elif (self.event_seq[0]['type'] == 2):
            event_code='Q'
        temp_info = self.module['info'].info_collect(time=self.currentTime, event=event_code,\
         uti=(self.module['node'].get_tot()-self.module['node'].get_idle())*1.0/self.module['node'].get_tot(),\
         waitNum=len(self.module['job'].wait_list()), waitSize=self.module['job'].wait_size(),\
         waitCore=self.module['job'].wait_core_seconds(), inter=temp_inter)
        self.print_sys_info(temp_info)
        return
    
    def interface(self, sys_info = None):
        #self.debug.debug("# "+self.myInfo+" -- interface",5) 
        return
    
    def alg_adapt(self):
        #self.debug.debug("# "+self.myInfo+" -- alg_adapt",5) 
        return 0
    
    def window_adapt(self):
        #self.debug.debug("# "+self.myInfo+" -- window_adapt",5) 
        return 0
    
    def print_sys_info(self, sys_info):
        #self.debug.debug("# "+self.myInfo+" -- print_sys_info",5) 
        self.module['output'].print_sys_info(sys_info)
    
    def print_adapt(self, adapt_info):
        #self.debug.debug("# "+self.myInfo+" -- print_adapt",5) 
        self.module['output'].print_adapt(adapt_info)
    
    def print_result(self):
        #self.debug.debug("# "+self.myInfo+" -- print_result",5) 
        self.module['output'].print_sys_info()
        self.module['output'].print_reward_info()
        self.debug.debug(lvl=1)
        self.module['output'].print_result(self.module['job'])
        
