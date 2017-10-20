import IOModule.Log_print as Log_print

__metaclass__ = type

class Cqsim_sim:
    def __init__(self, module, debug = None, monitor = None, mon_para = None):
        self.myInfo = "Cqsim Sim"
        self.module = module
        self.debug = debug
        self.monitor = monitor
        self.mon_para = mon_para
        
        self.show_module_info()
        
        self.event_seq = []
        self.event_pointer = 0
        self.monitor_start = 0
        self.current_event = None
        self.job_num = len(self.module['job'].job_info())
        self.currentTime = self.module['job'].get_virtual_start_time()
        self.startTime = self.currentTime
        
        self.debug.line(4)
        for module_name in self.module:
            temp_name = self.module[module_name].myInfo
            self.debug.debug(temp_name+" ................... Load",4)
            self.debug.line(4)
            
        
    def reset(self, module = None, debug = None, monitor = None, mon_para = None):
        #self.debug.debug("# "+self.myInfo+" -- reset",5)
        if module:
            self.module = module
        
        if debug:
            self.debug = debug
        if monitor:
            self.monitor = monitor
        if mon_para:
            self.mon_para = mon_para
               
            
        self.event_seq = []
        self.event_pointer = 0
        self.monitor_start = 0
        self.current_event = None
        self.job_num = len(self.module['job'].job_info())
        self.currentTime = self.module['job'].get_virtual_start_time()
        self.startTime = self.currentTime
        
    def show_module_info (self):
        #self.debug.line(1," ")
        self.debug.debug("-- "+self.myInfo,1)   
        
    def cqsim_sim(self):
        #self.debug.debug("# "+self.myInfo+" -- cqsim_sim",5)
        self.module['info'].reset_start_date(self.module['job'].get_start_date())
        self.insert_event_job()
        self.insert_event_extend()
        self.scan_event()
        self.print_result()
        self.debug.debug("------ Simulating Done!",2) 
        return
    
    def insert_event_job(self):
        #self.debug.debug("# "+self.myInfo+" -- insert_event_job",5) 
        i = 0
        x = 0
        while (i < self.job_num):
            self.insert_event(1,self.module['job'].job_info(i)['submit'],2,[1,i],1)
            #self.debug.debug("  "+"Insert job["+"2"+"] "+str(self.module['job'].job_info(i)['submit']),4)
            i += 1
            if (i>=x*5000):
                x += 1
                print i  
        return
    
    def insert_event_monitor(self, start, end):
        #self.debug.debug("# "+self.myInfo+" -- insert_event_monitor",5) 
        if (not self.monitor):
            return -1
        temp_num = (start-self.startTime)/self.monitor
        temp_num = int(temp_num)
        temp_time = temp_num*self.monitor + self.startTime
        while (temp_time < end):
            if (temp_time>=start):
                self.insert_event(2,temp_time,5,self.mon_para)
                #self.debug.debug("  "+"Insert mon["+"5"+"] "+str(temp_time),1)
            temp_time += self.monitor
        return
    
    def insert_event_extend(self):
        #self.debug.debug("# "+self.myInfo+" -- insert_event_extend",5) 
        return
    
    def insert_event(self, type, time, priority, para = None, quick = -1):
        #self.debug.debug("# "+self.myInfo+" -- insert_event",5) 
        temp_index = -1
        new_event = {"type":type, "time":time, "prio":priority, "para":para}
        if quick == -1 :
            if (type == 1):
                i = self.event_pointer
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
        if (self.event_pointer>=self.monitor_start):
            self.monitor_start=self.event_pointer+1
        temp_mon = self.monitor_start
        self.monitor_start += 1
        return temp_mon
    
    def scan_event(self):
        # self.debug.debug("# "+self.myInfo+" -- scan_event",5) 
        self.debug.line(2," ")
        self.debug.line(2,"=")
        self.debug.line(2,"=")
        self.current_event = None
        self.print_adapt()
        while (self.event_pointer < len(self.event_seq)):
            self.current_event = self.event_seq[self.event_pointer]
            self.currentTime = self.current_event['time']
            if (self.current_event['type'] == 1):
                self.debug.line(2," ") 
                self.debug.line(2,">>>") 
                self.debug.line(2,"--") 
                print ("  Time: "+str(self.currentTime)) 
                self.debug.debug("  Time: "+str(self.currentTime) + \
                                 "  Tot:"+str(self.module['node'].get_tot())+\
                                 "  Idle:"+str(self.module['node'].get_idle())+\
                                 "  Avail:"+str(self.module['node'].get_avail()),2) 
                self.debug.debug("   "+str(self.current_event),2)
                self.debug.line(2,"--") 
                self.debug.debug("  Wait: "+str(self.module['job'].wait_list()),2) 
                self.debug.debug("  Run : "+str(self.module['job'].run_list()),2) 
                self.debug.line(2,"--") 
                
                self.event_job(self.current_event['para'])
            elif (self.current_event['type'] == 2):
                self.event_monitor(self.current_event['para'])
            elif (self.current_event['type'] == 3):
                self.event_extend(self.current_event['para'])
            self.interface()
            self.event_pointer += 1
            
            
        if (self.monitor):
            self.insert_event(2,self.currentTime,5,self.mon_para)
            self.current_event = self.event_seq[self.event_pointer]
            self.event_monitor(self.current_event['para'])
        self.debug.line(2,"=")
        self.debug.line(2,"=")
        self.debug.line(2," ")
        
        return
    
    def event_job(self, para_in = None):
        #self.debug.debug("# "+self.myInfo+" -- event_job",5) 
        if (self.current_event['para'][0] == 1):
            self.submit(self.current_event['para'][1])
        elif (self.current_event['para'][0] == 2):
            self.finish(self.current_event['para'][1])
        self.score_calculate()
        self.start_scan()
        if (self.event_pointer < len(self.event_seq)-1):
            self.insert_event_monitor(self.currentTime, self.event_seq[self.event_pointer+1]['time'])
        return
    
    def event_monitor(self, para_in = None):
        #self.debug.debug("# "+self.myInfo+" -- event_monitor",5) 
        self.sys_collect(self.event_seq[self.event_pointer])
        need_print = 0
        need_print += self.backfill_adapt()
        need_print += self.alg_adapt()
        need_print += self.window_adapt()
        if (need_print):
            self.print_adapt()
        return
    
    def event_extend(self, para_in = None):
        #self.debug.debug("# "+self.myInfo+" -- event_extend",5) 
        return
    
    def submit(self, job_index):
        #self.debug.debug("# "+self.myInfo+" -- submit",5) 
        self.debug.debug("[Submit]  "+str(job_index),3)
        self.module['job'].job_submit(job_index)
        self.sys_collect(self.event_seq[self.event_pointer])
        return
    
    def finish(self, job_index):
        #self.debug.debug("# "+self.myInfo+" -- finish",5) 
        self.debug.debug("[Finish]  "+str(job_index),3)
        self.module['node'].node_release(job_index,self.currentTime)
        self.module['job'].job_finish(job_index)
        self.sys_collect(self.event_seq[self.event_pointer])   
        return
    
    def start(self, job_index):
        #self.debug.debug("# "+self.myInfo+" -- start",5) 
        self.debug.debug("[Start]  "+str(job_index),3)
        temp_node_req = {'proc':self.module['job'].job_info(job_index)['usedProc']}
        node_list = self.module['node'].node_allocate(temp_node_req, job_index,\
         self.currentTime, self.currentTime + self.module['job'].job_info(job_index)['reqTime'])
        self.module['job'].job_start(job_index, self.currentTime, node_list)
        self.insert_event(1,self.currentTime+self.module['job'].job_info(job_index)['run'],1,[2,job_index])
        self.sys_collect({"type":1, "time":self.currentTime, "prio":0, "para":[3,job_index]})
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
            temp_node_req = {'proc':temp_job['reqProc']}
            if (self.module['node'].is_available(temp_node_req)):
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
        #print "## ",temp_wait_A,temp_wait_B

        temp_wait_info = []
        max_num = len(temp_wait_A)
        i = 0
        while (i < max_num):
            temp_job = self.module['job'].job_info(temp_wait_A[i])
            temp_req_node = {"proc":temp_job['reqProc']}
            temp_wait_info.append({"index":temp_wait_A[i],"reqNodes":temp_req_node,\
             "run":temp_job['run'],"score":temp_job['score']})
            i += 1 
            
        #print "### ",temp_wait_info
        temp_wait_A = self.module['win'].start_window(temp_wait_info,{"time":self.currentTime})
        #print "# ",temp_wait_A,temp_wait_B
        temp_wait_B[0:0] = temp_wait_A
        return temp_wait_B
    
    def backfill(self, temp_wait):
        #self.debug.debug("# "+self.myInfo+" -- backfill",5) 
        temp_wait_info = []
        max_num = len(temp_wait)
        i = 0
        while (i < max_num):
            temp_job = self.module['job'].job_info(temp_wait[i])
            temp_req_node = {"proc":temp_job['reqProc']}
            temp_wait_info.append({"index":temp_wait[i],"reqNodes":temp_req_node,\
             "run":temp_job['run'],"score":temp_job['score']})
            i += 1
        backfill_list = self.module['backfill'].backfill(temp_wait_info, {'time':self.currentTime})
        '''
        try:
            while (i < max_num):
                temp_job = self.module['job'].job_info(temp_wait[i])
                temp_wait_info.append({"index":temp_wait[i],"proc":temp_job['reqProc'],\
                 "node":temp_job['reqProc'],"run":temp_job['run'],"score":temp_job['score']})
                i += 1
        except:
            print "11111111111111111111"
        try:
            backfill_list = self.module['backfill'].backfill(temp_wait_info, {'time':self.currentTime})
        except:
            print "2222222222222222222"
        '''
        #self.debug.debug("HHHHHHHHHHHHH "+str(backfill_list)+" -- backfill",2) 
        if not backfill_list:
            return 0
        
        for job in backfill_list:
            self.debug.debug("[BACKFILL]",3,0) 
            self.start(job)
        return 1
    
    def sys_collect(self,sys_info_list):
        #self.debug.debug("# "+self.myInfo+" -- sys_collect",5)         
        event_code=None
        temp_para=None
        if (sys_info_list['type'] == 1):
            if (sys_info_list['para'][0] == 1):   
                event_code='Q'
            elif(sys_info_list['para'][0] == 3):   
                event_code='S'
                temp_para=self.module['job'].job_info(sys_info_list['para'][1])
            elif(sys_info_list['para'][0] == 2):   
                event_code='E'
                temp_para=self.module['job'].job_info(sys_info_list['para'][1])
        elif (sys_info_list['type'] == 2):
            event_code='C'
            temp_para=sys_info_list['para']
        #print "-------",event_code,(self.module['node'].get_tot()-self.module['node'].get_idle())*1.0/self.module['node'].get_tot()
        self.module['info'].info_collect(time=self.currentTime, event=event_code,\
         uti=(self.module['node'].get_tot()-self.module['node'].get_idle())*1.0/self.module['node'].get_tot(), current_para = temp_para)
        self.module['backfill'].set_adapt_data()
        self.module['alg'].set_adapt_data()
        self.module['win'].set_adapt_data()
        #self.debug.debug(">>>>>>>>>>>>>>>   "+str(self.module['info'].get_info(self.module['info'].get_len()-1)),2) 
        self.print_sys_info(self.module['info'].get_info(self.module['info'].get_current_index()))
        return
    
    def interface(self, sys_info = None):
        #self.debug.debug("# "+self.myInfo+" -- interface",5) 
        return
    
    def backfill_adapt(self):
        #self.debug.debug("# "+self.myInfo+" -- backfill_adapt",5)
        adapt_result = 0 
        adapt_result += self.module['backfill'].backfill_adapt()
        return adapt_result
    
    def alg_adapt(self):
        #self.debug.debug("# "+self.myInfo+" -- alg_adapt",5) 
        adapt_result = 0
        adapt_result += self.module['alg'].alg_adapt()
        return adapt_result
    
    def window_adapt(self):
        #self.debug.debug("# "+self.myInfo+" -- window_adapt",5) 
        adapt_result = 0
        adapt_result += self.module['win'].window_adapt()
        return adapt_result
    
    def print_sys_info(self, sys_info):
        #self.debug.debug("# "+self.myInfo+" -- print_sys_info",5) 
        self.module['output'].print_sys_info(sys_info)
    
    def print_adapt(self):
        #self.debug.debug("# "+self.myInfo+" -- print_adapt",5) 
        adapt_info = []
        adapt_info[0:0] = self.module['backfill'].get_adapt_list()
        adapt_info[0:0] = self.module['alg'].get_adapt_list()
        adapt_info[0:0] = self.module['win'].get_adapt_list()
        adapt_info.insert(0,self.currentTime)
        self.module['output'].print_adapt(adapt_info)
    
    def print_result(self):
        #self.debug.debug("# "+self.myInfo+" -- print_result",5) 
        self.module['output'].print_result(self.module['job'])
        
