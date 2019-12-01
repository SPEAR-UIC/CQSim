import IOModule.Log_print as Log_print

__metaclass__ = type

class Cqsim_sim:
    def __init__(self, module, debug = None, monitor = None):
        self.myInfo = "Cqsim Sim"
        self.module = module
        self.debug = debug
        self.monitor = monitor
        
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
        
        self.debug.line(4)
        for module_name in self.module:
            temp_name = self.module[module_name].myInfo
            self.debug.debug(temp_name+" ................... Load",4)
            self.debug.line(4)
        
    def reset(self, module = None, debug = None, monitor = None):
        #self.debug.debug("# "+self.myInfo+" -- reset",5)
        if module:
            self.module = module
        
        if debug:
            self.debug = debug
        if monitor:
            self.monitor = monitor
               
            
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
        
    def cqsim_sim(self):
        #self.debug.debug("# "+self.myInfo+" -- cqsim_sim",5)
        #self.insert_submit_events()
        self.import_submit_events()
        #self.insert_event_job()
        self.insert_event_extend()
        self.scan_event()
        self.print_result()
        self.debug.debug("------ Simulating Done!",2) 
        self.debug.debug(lvl=1) 
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
        self.score_calculate()
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
    
    def start_scan(self):
        #self.debug.debug("# "+self.myInfo+" -- start_scan",5) 
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
        while (i < max_num):
            temp_job = self.module['job'].job_info(temp_wait[i])
            temp_wait_info.append({"index":temp_wait[i],"proc":temp_job['reqProc'],\
             "node":temp_job['reqProc'],"run":temp_job['run'],"score":temp_job['score']})
            i += 1
        backfill_list = self.module['backfill'].backfill(temp_wait_info, {'time':self.currentTime})
        #self.debug.debug("HHHHHHHHHHHHH "+str(backfill_list)+" -- backfill",2) 
        if not backfill_list:
            return 0
        
        for job in backfill_list:
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
         waitNum=len(self.module['job'].wait_list()), waitSize=self.module['job'].wait_size(), inter=temp_inter)
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
        self.debug.debug(lvl=1)
        self.module['output'].print_result(self.module['job'])
        
