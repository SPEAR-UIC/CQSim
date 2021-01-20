from random import *
import math
import copy
import time
import IOModule.Log_print as Log_print


__metaclass__ = type

class Cqsim_sim:
    def __init__(self, module, debug = None, monitor = None, schedule = "F", win_size = 10, generations = 50):
        self.myInfo = "Cqsim Sim"
        self.module = module
        self.debug = debug
        self.monitor = monitor
        self.schedule = schedule
        self.win_size = win_size
        self.generations = generations
        
        self.debug.line(4," ")
        self.debug.line(4,"#")
        self.debug.debug("# "+self.myInfo,1)
        self.debug.line(4,"#")
        
        self.event_seq = []
        self.event_pointer = 0
        self.monitor_start = 0
        self.current_event = None
        self.job_num = len(self.module['job'].job_info())
        self.currentTime = 0
        self.avg_distance_list = []
        self.util_list = []
        self.time_list = []

        
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
        self.event_pointer = 0
        self.monitor_start = 0
        self.current_event = None
        self.job_num = len(self.module['job'].job_info())
        self.currentTime = 0
        self.avg_distance_list = []
        self.util_list = []
        self.time_list = []
        
    def cqsim_sim(self):
        #self.debug.debug("# "+self.myInfo+" -- cqsim_sim",5)
        self.insert_event_job()
        self.insert_event_extend()
        self.scan_event()
        self.print_result()
        self.debug.debug("------ Simulating Done!",2) 
        return
    
    def insert_event_job(self):
        #self.debug.debug("# "+self.myInfo+" -- insert_event_job",5) 
        i = 0
        while (i < self.job_num):
            self.insert_event(1,self.module['job'].job_info(i)['submit'],2,[1,i])
            #self.debug.debug("  "+"Insert job["+"2"+"] "+str(self.module['job'].job_info(i)['submit']),4)
            i += 1
        return
    
    def insert_event_monitor(self, start, end):
        #self.debug.debug("# "+self.myInfo+" -- insert_event_monitor",5) 
        if (not self.monitor):
            return -1
        temp_num = start/self.monitor
        temp_num = int(temp_num)
        temp_time = temp_num*self.monitor
        i = 0
        while (temp_time < end):
            if (temp_time>=start):
                self.insert_event(2,temp_time,5,None)
                #self.debug.debug("  "+"Insert mon["+"5"+"] "+str(temp_time),4)
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
        while (self.event_pointer < len(self.event_seq)):
            self.current_event = self.event_seq[self.event_pointer]
            self.currentTime = self.current_event['time']
            if (self.current_event['type'] == 1):
                self.debug.line(2," ") 
                self.debug.line(2,">>>") 
                self.debug.line(2,"--") 
                print ("  Time: "+str(self.currentTime)) 
                self.debug.debug("  Time: "+str(self.currentTime),2) 
                self.debug.debug("   "+str(self.current_event),2)
                self.debug.line(2,"--")
                if len(self.module['job'].wait_list()) < 20:
                    self.debug.debug("  Wait: "+str(self.module['job'].wait_list()),2) 
                if len(self.module['job'].run_list()) < 20:
                    self.debug.debug("  Run : "+str(self.module['job'].run_list()),2) 
                self.debug.line(2,"--") 
                self.debug.debug("  Tot:"+str(self.module['node'].get_tot())+" Idle:"+str(self.module['node'].get_idle())+" Avail:"+str(self.module['node'].get_avail())+" Avail_Ran:"+str(self.module['node'].get_ran_avail())+" ",2)
                self.debug.line(2,"--") 
                
                self.event_job(self.current_event['para'])
            elif (self.current_event['type'] == 2):
                self.event_monitor(self.current_event['para'])
            elif (self.current_event['type'] == 3):
                self.event_extend(self.current_event['para'])
            self.sys_collect()
            self.interface()
            self.event_pointer += 1
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
        #print 'event_job',self.current_event['para']
        if (self.current_event['para'][0] == 1):
            self.submit(self.current_event['para'][1])
        elif (self.current_event['para'][0] == 2):
            self.finish(self.current_event['para'][1])
        #elif (self.current_event['para'][0] == 3):
        #    self.submit_job_after_stage_in(self.current_event['para'][1])
        #elif (self.current_event['para'][0] == 4):
        #    self.submit_job_without_stage_in(self.current_event['para'][1])
        #elif (self.current_event['para'][0] == 5):
        #    self.module['bb'].bb_release(self.current_event['para'][1])
        #    self.module['job'].job_stage_out_end(self.current_event['para'][1])
        self.score_calculate()
        #self.start_scan_bb()
        self.start_scan()
        if (self.event_pointer < len(self.event_seq)-1):
            self.insert_event_monitor(self.currentTime, self.event_seq[self.event_pointer+1]['time'])
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
        #self.debug.debug("[Finish]  "+str(job_index),3)
        self.module['node'].node_release(job_index,self.currentTime)
        '''
        if (self.module['job'].job_info(job_index)['reqRan'] > 0):
            if (self.module['job'].job_info(job_index)['stageOutTime'] > 0):
                self.insert_event(1,self.currentTime+self.module['job'].job_info(job_index)['stageOutTime'],1,[5,job_index])
            else:
                self.module['bb'].bb_release(job_index)
        '''
        self.module['job'].job_finish(job_index,self.currentTime)
        self.debug.debug("  Tot:"+str(self.module['node'].get_tot())+" Idle:"+str(self.module['node'].get_idle())+" Avail:"+str(self.module['node'].get_avail())+" Avail_Ran:"+str(self.module['node'].get_ran_avail())+" ",2)
        return
    
    def start(self, job_index):
        #self.debug.debug("# "+self.myInfo+" -- start",5) 
        self.debug.debug("[Start]  "+str(job_index),3)
        self.module['node'].node_allocate(self.module['job'].job_info(job_index)['reqProc'], job_index,\
         self.currentTime, self.currentTime + self.module['job'].job_info(job_index)['reqTime'],self.module['job'].job_info(job_index)['reqRan'])
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
        '''
        print temp_wait
        temp_wait.reverse()
        print temp_wait
        '''
        ###################
        #'''
        if self.schedule != "F":
            win_size = self.win_size
            if len(temp_wait)<win_size:
                win_size = len(temp_wait)
            if win_size > 2:
                resource_num = len(self.module['job'].job_info(temp_wait[0])['reqRan']) + 1
                #resource_num = len(rank1_exhaustive[rank1_exhaustive.keys()[0]]['ran_util']) + 1
                w = [1.0/resource_num]*resource_num
                time_sig = ';'
                time_str = str(win_size)+time_sig
                start_time = time.time()
                rank1 = self.ga(win_size,temp_wait)
                if len(rank1) > 0:
                    best_key_ga = self.best_from_ga(rank1)
                    time_str += str(time.time()-start_time)
                    start_time = time.time()
                    best_key_bin = self.bin_packing(win_size,temp_wait, w)
                    time_str += ';'+str(time.time()-start_time)
                    self.time_list.append(time_str)
                    temp_job_info_list = []
                    i = 0
                    while(i<win_size):
                        temp_job = self.module['job'].job_info(temp_wait[i])
                        temp_job_info_list.append(temp_job)
                        i += 1
                    d_ga = self.compute_fitness_value(best_key_ga,temp_job_info_list)
                    d_bin = self.compute_fitness_value(best_key_bin,temp_job_info_list)
                    temp_util = str(d_ga['util'])+','+str(d_bin['util'])
                    for x,y in zip(d_ga['ran_util'],d_bin['ran_util']):
                        temp_util += ';'+str(x)+','+str(y)

                    self.util_list.append(temp_util)                    
                    if self.schedule == "M":
                        temp_wait = self.update_wait_order(temp_wait,best_key_ga)
                    elif self.schedule == "B":
                        temp_wait = self.update_wait_order(temp_wait,best_key_bin)
                    self.module['job'].update_wait_list(temp_wait)
                '''
                if self.schedule == "M":
                    rank1 = self.ga(win_size,temp_wait)
                    if len(rank1) > 0:
                        best_key = self.best_from_ga(rank1)
                elif self.schedule == "E":
                    temp_job_info_list = []
                    i = 0
                    while(i<win_size):
                        temp_job = self.module['job'].job_info(temp_wait[i])
                        temp_job_info_list.append(temp_job)
                        i += 1
                    rank1 = self.exhaustive(temp_job_info_list)
                    best_key = self.best_from_ga(rank1)
                elif self.schedule == "W":
                    best_key = self.weighted_recursive(win_size,temp_wait, w)
                elif self.schedule == "B":
                    best_key = self.bin_packing(win_size,temp_wait, w)
                if len(rank1) > 0:
                    time_str += str(time.time()-start_time)
                    self.time_list.append(time_str)

                    temp_job_info_list = []
                    i = 0
                    while(i<win_size):
                        temp_job = self.module['job'].job_info(temp_wait[i])
                        temp_job_info_list.append(temp_job)
                        i += 1
                    d = self.compute_fitness_value(best_key,temp_job_info_list)
                    temp_util = str(d['util'])
                    for x in d['ran_util']:
                        temp_util += ';'+str(x)
                    self.util_list.append(temp_util)

                    if (self.schedule == "M" or self.schedule == "B"):
                        if len(best_key) <= 15:
                            rank1_exhaustive = self.exhaustive(temp_job_info_list)
                            self.compute_avg_distance(rank1, rank1_exhaustive)
                        else:
                            self.avg_distance_list.append(-1)
                    '''

        ###################
        wait_num = len(temp_wait)
        win_count = start_max
            
        i = 0
        while (i<wait_num):
            if (win_count >= start_max):
                win_count = 0
                #print "temp_wait_before"
                #print temp_wait
                temp_wait = self.start_window(temp_wait)
                #print "temp_wait_after"
                #print temp_wait
            #print "....  ", temp_wait[i]
            #print '+++++++'
            #print "i:",str(i),"wait_num:",wait_num,"start_max",start_max,"win_count",win_count,"temp_wait:",temp_wait
            #print '+++++++'
            temp_job = self.module['job'].job_info(temp_wait[i])
            #print "ReqProcRan:",temp_job['reqProc'],temp_job['reqRan']
            reqRan = temp_job['reqRan']
            if reqRan < 0:
                reqRan = 0
            if (self.module['node'].is_available(temp_job['reqProc'],temp_job['reqRan'])):
                self.start(temp_wait[i])
                #print "Start"
            else:
                temp_wait = self.module['job'].wait_list()
                self.backfill(temp_wait)
                #print "Backfill++++++++"
                break
            i += 1
            win_count += 1
        return

    ###################

    def compute_avg_distance(self, rank1_ga, rank1_exhaustive):
        ranks_ga = rank1_ga.keys()
        ranks_exhaustive = rank1_exhaustive.keys()
        dist = 0
        for rank in ranks_ga:
            if rank not in ranks_exhaustive:
                smallest_distance = 0
                for rank_e in ranks_exhaustive:
                    dis = 0
                    for i in range(len(rank_e)):
                        if rank[i] != rank_e[i]:
                            dis += 1
                    if dis > smallest_distance:
                        smallest_distance = dis
                dist += smallest_distance
        if len(ranks_ga) > 0:
            self.avg_distance_list.append(dist/len(ranks_ga))

    def update_wait_order(self,temp_wait,best_key):
        temp_es = []
        temp_temp_wait = copy.deepcopy(temp_wait)
        i = len(best_key) -1
        while(i >= 0):
            if best_key[i] == '1':
                temp_es.append(temp_wait[i])
                del temp_temp_wait[i]
            i -= 1
        temp_es.reverse()
        temp_temp_temp_wait = temp_es + temp_temp_wait
        return temp_temp_temp_wait

    def subtract_resource_usage(self, job_info, W):
        W[0] -= job_info['reqProc']
        for i in range(len(job_info['reqRan'])):
            W[i+1] -= job_info['reqRan'][i]

    def fit_to_system(self, job_info, W):
        if job_info['reqProc'] > W[0]:
            return False
        for i in range(len(job_info['reqRan'])):
            if job_info['reqRan'][i] > W[i+1]:
                return False
        return True

    def compute_alignment_score(self,job_info, W, w):
        score = job_info['reqProc']*W[0]*w[0]
        for i in range(len(job_info['reqRan'])):
            score += job_info['reqRan'][i]*W[i+1]*w[i+1]
        return score

    def bin_packing(self,win_size,temp_wait,w):
        temp_job_info_list = []
        i = 0
        while(i<win_size):
            temp_job = self.module['job'].job_info(temp_wait[i])
            temp_job_info_list.append(temp_job)
            i += 1
        #temp_job_info_copy = copy.deepcopy(temp_job_info_list)
        W = [self.module['node'].get_avail()]
        W = W + copy.deepcopy(self.module['node'].get_ran_avail())

        # 0: not selected; 1: selected; 2: too large to be selected
        job_select = ['0']*win_size

        while ('0' in job_select):
            highest_score = -1
            job_position = -1
            for i in range(len(temp_job_info_list)):
                if (job_select[i] == '1' or job_select[i] == '2'):
                    continue
                else:
                    if not self.fit_to_system(temp_job_info_list[i], W):
                        job_select[i] = '2'
                        continue
                    else:
                        score = self.compute_alignment_score(temp_job_info_list[i], W, w)
                        if score > highest_score:
                            highest_score = score
                            job_position = i
            if (highest_score<0 or job_position<0):
                break
            job_select[job_position] = '1'
            self.subtract_resource_usage(temp_job_info_list[job_position],W)
        for x in range(len(job_select)):
            if job_select[x] == '2':
                job_select[x] = '0'
        str_job_select = ''.join(job_select)
        return str_job_select

    def knapSack(self, W , wt , val , n, s): 
        if n == 0: 
            return 0
        for w in W:
            if w == 0:
                return 0
        for i in range(len(W)):
            if (wt[i][n-1] > W[i]):
                return self.knapSack(W , wt , val , n-1, s) 
        Wt = copy.deepcopy(W)
        for x in range(len(Wt)):
            Wt[x] -= wt[x][n-1]
        v1 = val[n-1] + self.knapSack(Wt , wt , val , n-1, s)
        v2 = self.knapSack(W , wt , val , n-1, s)
        if v1 >= v2:
            s.add(n-1)
            return v1
        else:
            return v2

    def weighted_recursive(self, win_size, temp_wait, w):
        temp_job_info_list = []
        i = 0
        while(i<win_size):
            temp_job = self.module['job'].job_info(temp_wait[i])
            temp_job_info_list.append(temp_job)
            i += 1
        val = []
        wt = []
        res_num = len(temp_job_info_list[0]['reqRan'])+1
        for i in range(res_num):
            wt.append([])
        for temp_job_info in temp_job_info_list:
            val_temp = w[0]*temp_job_info['usedProc']/self.module['node'].get_tot()
            wt[0].append(temp_job_info['usedProc'])
            x = 1
            for temp_ran in temp_job_info['reqRan']:
                val_temp += w[x]*temp_ran/self.module['node'].get_ran_vol_tot()[x-1]
                wt[x].append(temp_ran)
                x += 1
            val.append(val_temp)

        W = [self.module['node'].get_avail()]
        W = W + copy.deepcopy(self.module['node'].get_ran_avail())
        n = len(val) 
        s = set()
        self.knapSack(W , wt , val , n, s)
        job_select = ['0']*n
        for i in s:
            job_select[i] = '1'
        str_job_select = ''.join(job_select)
        return str_job_select

    def best_from_weighted(self,rank1, weight):
        best_score = -1
        best_key = "-1"
        for k,v in rank1.items():
            temp_score = weight[0]*v["util"]
            for x in range(len(v["ran_util"])):
                temp_score += weight[x+1]*v["ran_util"][x]
            if temp_score > best_score:
                best_score = temp_score
                best_key = k
        return best_key

    def best_from_ga(self,rank1):
        best_score = -1
        best_key = "-1"
        for k,v in rank1.items():
            temp_score = v["util"]
            if temp_score > best_score:
                best_score = temp_score
                best_key = k
        best_value = rank1[best_key]
        #temp_best_score = best_value["ssd_util"] + best_value["bb_util"]
        temp_best_score = 0
        for key in best_value.keys():
            if (key == "util") or (key == "age"):
                continue
            if not isinstance(best_value[key], list):
               temp_best_score += best_value[key]
            else:
                for x in best_value[key]:
                    temp_best_score += x
        #temp_best_score = best_value["wasted_BB_time"]
        #best_key_temp_list = []
        best_key_temp = "-1"
        best_temp_score = -1
        for k,v in rank1.items():
            if k != best_key:
                #temp_score = v["ssd_util"] + v["bb_util"]
                temp_score = 0
                for key in v.keys():
                    if (key == "util") or (key == "age"):
                        continue
                    if not isinstance(v[key],list):
                        temp_score += v[key]
                    else:
                        for x in v[key]:
                            temp_score += x
                #temp_score = v["wasted_BB_time"]
                if (temp_score - temp_best_score) > 0.3*abs(temp_best_score):
                    if best_value["util"] - v["util"] < 0.1:
                        #best_key_temp_list.append(k)
                        if temp_score > best_temp_score:
                            best_key_temp = k
                            best_temp_score = temp_score
        if best_temp_score > 0:
            best_key = best_key_temp
        return best_key

#++++++++++++++++

    def exhaustive(self,temp_job_info_list):
        lists = ['0', '1']
        for _ in range(len(temp_job_info_list)-1):
            lists = ['0'+x for x in lists] + ['1'+x for x in lists]
        #print('lists',lists)

        population = {}
        for possible_solution in lists:
            d = self.compute_fitness_value(possible_solution,temp_job_info_list)
            if self.is_fesible(d):
                population[possible_solution] = copy.deepcopy(d)
                population[possible_solution]['age'] = 0
        rank1, rank2 = self.get_pareto_front(population)
        return rank1

    '''
    temp_population = {}
        popluation_size = int(math.ceil(2**win_size/50))
        if popluation_size < 10:
            popluation_size = 10
        if 2**win_size < 10:
            popluation_size = 2**win_size
        i = 0
        j = 0
        while(i < popluation_size):
            ri = randint(0,2**win_size-1)
            form = "{0:0"+str(win_size)+"b}"
            temp_index = form.format(ri)
            if temp_index in temp_population:
                continue
            if temp_index in not_fes_list:
                continue
            d = self.compute_fitness_value(temp_index,temp_job_info_list)
            if not self.is_fesible(d):
                not_fes_list.append(temp_index)
                i += 1
                continue

            temp_population[temp_index] = copy.deepcopy(d)
            temp_population[temp_index]['age'] = 0
            #temp_population[temp_index] = {"util":util,"ipower":ipower,"ran_util":ran_util,"age":0}
            i += 1
        return temp_population,not_fes_list,popluation_size
    '''

    def unfit_padding(self,rank1_temp,job_eliminate_list):
        rank1 = {}
        for k,v in rank1_temp.items():
            k_list = list(k)
            for i in range(len(job_eliminate_list)):
                if job_eliminate_list[i] == '0':
                    k_list.insert(i, 0)
                    i += 1
                i += 1
            k_str = ''.join(k_list)
            rank1[k_str] = v
        return rank1

    def ga(self, win_size,temp_wait):
        temp_job_info_list = []
        not_fes_list = []
        job_eliminate_list = ['1']*win_size
        i = 0
        temp_win_size = win_size
        while(i<win_size):
            temp_job = self.module['job'].job_info(temp_wait[i])
            if (self.module['node'].is_available(temp_job['reqProc'],temp_job['reqRan'])):
                temp_job_info_list.append(temp_job)
            else:
                job_eliminate_list[i] = '0'
                temp_win_size -= 1
            i += 1
        if temp_win_size <= 0:
            return {}
        elif temp_win_size <= 10:
            temp_temp_wait = copy.deepcopy(temp_wait)
            x = len(temp_temp_wait)
            for _ in range(len(temp_temp_wait)):
                x -= 1
                if job_eliminate_list[x] == '0':
                    del temp_temp_wait[x]
            rank1_temp = self.exhaustive(temp_job_info_list)
            rank1 = self.unfit_padding(rank1_temp,job_eliminate_list)
            return rank1

        #print ".....init_population......"
        start_time = time.time()
        population,not_fes_list_temp,population_size = self.init_population(temp_win_size,temp_job_info_list,not_fes_list)
        not_fes_list += not_fes_list_temp
        not_fes_list = list(set(not_fes_list))
        self.debug.debug(".....init_population"+' '+str(float(time.time()-start_time))+' '+str(len(population)),5)

        #print ".....get_pareto_front......"
        start_time = time.time()
        rank1, rank2 = self.get_pareto_front(population)
        self.debug.debug(".....get_pareto_front"+' '+str(float(time.time()-start_time))+' '+str(len(population)),5)
        pc=1.0
        pm=0.05

        generations = self.generations
        if generations > int(math.ceil(0.1*2**temp_win_size)):
            generations = int(math.ceil(0.1*2**temp_win_size))
        i = 0
        while(i<generations):

            if len(rank1) <= 0:
                print ".........len(rank1) <= 0............"
                break

            #print ".....parent_selection......",str(i)
            start_time = time.time()
            temp_population = copy.deepcopy(population)
            parents_list = self.parent_selection(rank1,rank2,0.7,int(math.floor(0.5*population_size)),temp_population)
            #parents_list = self.parent_selection(rank1,rank2,0.7,int(math.floor(pc*population_size)))
            self.debug.debug(".....parent_selection"+' '+str(i)+' '+str(float(time.time()-start_time))+' '+str(len(population)),5)

            #print ".....crossover......",str(i)
            start_time = time.time()
            off_springs,not_fes_list_temp = self.crossover(parents_list,temp_job_info_list,population.keys()+not_fes_list)
            not_fes_list += not_fes_list_temp
            not_fes_list = list(set(not_fes_list))
            self.debug.debug(".....crossover"+' '+str(i)+' '+str(float(time.time()-start_time))+' '+str(len(population)),5)

            #print ".....mutation......",str(i)
            start_time = time.time()
            mut_off_springs, not_fes_list_temp = self.mutation(population,off_springs,not_fes_list,temp_job_info_list,pm)
            not_fes_list += not_fes_list_temp
            not_fes_list = list(set(not_fes_list))
            self.debug.debug(".....mutation"+' '+str(i)+' '+str(float(time.time()-start_time))+' '+str(len(population)),5)

            #print ".....survior_selection......",str(i)
            start_time = time.time()
            #population_size = int(math.floor(population_size*1.00))
            rank1, rank2, population = self.survior_selection(rank1,rank2,off_springs,mut_off_springs,population_size)
            self.debug.debug(".....survior_selection"+' '+str(i)+' '+str(float(time.time()-start_time))+' '+str(len(population)),5)
            #print 'population size: ',len(population)

            i += 1
        rank1 = self.unfit_padding(rank1,job_eliminate_list)
        return rank1



    def survior_selection(self,rank1,rank2,off_springs,mut_off_springs,population_size):
        temp_dict1 = self.merge_two_dicts(rank1,off_springs)
        temp_dict = self.merge_two_dicts(temp_dict1,mut_off_springs)
        #prinpopulation size: t('temp_dict',temp_dict)
        rank1_temp, rank2_temp1 = self.get_pareto_front(temp_dict)
        rank2_temp = self.merge_two_dicts(rank2_temp1,rank2)

        # get_rid_of oldest #
        while(len(rank1_temp)<population_size and len(rank1_temp)+len(rank2_temp)>population_size):
            oldest_age = -1
            temp_key = "-1"
            if len(rank2_temp) <= 0:
                break
            for k,v in rank2_temp.items():
                if v["age"] > oldest_age:
                    oldest_age = v["age"]
                    temp_key = k
            if temp_key != "-1":
                del rank2_temp[temp_key]

        if len(rank1_temp) >= population_size:
            rank2_temp = {}
            while len(rank1_temp) > population_size:
                del rank1_temp[rank1_temp.keys()[randint(0,len(rank1_temp)-1)]]

        rank1_temp = self.aging(rank1_temp)
        rank2_temp = self.aging(rank2_temp)
        population_temp = self.merge_two_dicts(rank1_temp,rank2_temp)
        return rank1_temp, rank2_temp, population_temp

    def aging(self,population):
        for k,v in population.items():
            population[k]["age"] = population[k]["age"] + 1
        return population

    def mutation(self,population,off_springs,not_fes_list,temp_job_info_list,pm):
        temp_population = self.merge_two_dicts(population,off_springs)
        mut_off_springs = {}
        not_fes_list_temp = []
        mut_num = int(math.floor(len(temp_population)*pm))
        i = 0
        while(i<mut_num):
            choice_key = choice(temp_population.keys())
            rand_pos = randint(0,len(choice_key))
            temp_key = ""
            for j in range(len(choice_key)):
                if j == rand_pos:
                    if choice_key[j] == '1':
                        temp_key += '0'
                    else:
                        temp_key += '1'
                else:
                    temp_key += choice_key[j]
            if temp_key in not_fes_list:
                i += 1
                continue
            if temp_key in temp_population.keys():
                i += 1
                continue
            d = self.compute_fitness_value(temp_key,temp_job_info_list)
            if not self.is_fesible(d):
                not_fes_list_temp.append(temp_key)
                #i += 1
                #continue
            else:
                mut_off_springs[temp_key] = copy.deepcopy(d)
                mut_off_springs[temp_key]['age'] = 0
                #mut_off_springs[temp_key] = {"util":util,"ipower":ipower,"ran_util":ran_util,"age":0}
            i += 1

        return mut_off_springs, not_fes_list_temp

    def merge_two_dicts(self,x, y):
        z = x.copy()
        z.update(y)
        return z

    def crossover(self,parents_list,temp_job_info_list,considered_list):
        off_springs = {}
        not_fes_list = []
        i = 0
        while(i<len(parents_list)):
            parents = parents_list[i]
            p1 = parents[0]
            p2 = parents[1]
            cut = len(p1)/2
            p1_temp = p1[:cut] + p2[cut:]
            p2_temp = p2[:cut] + p1[cut:]
            for temp_off_spring in [p1_temp,p2_temp]:
                if temp_off_spring in considered_list:
                    continue
                d = self.compute_fitness_value(temp_off_spring,temp_job_info_list)
                if not self.is_fesible(d):
                    not_fes_list.append(temp_off_spring)
                    #i += 1
                    #continue
                    ### to_do  ###
                else:
                    off_springs[temp_off_spring] = copy.deepcopy(d)
                    off_springs[temp_off_spring]['age'] = 0
                    #off_springs[temp_off_spring] = {"util":util,"ipower":ipower,"ran_util":ran_util,"age":0}
            i += 1
        return off_springs,not_fes_list

    '''
    def parent_selection(self,rank1,rank2,fav,parents_pair):
        parents_list = []
        if parents_pair <=0:
            parents_pair = 1
        i = 0
        while(i<parents_pair):
            if random()>fav:
                if len(rank2)-1 <= 0:
                    p1 = rank1.keys()[randint(0,len(rank1)-1)]
                else:
                    p1 = rank2.keys()[randint(0,len(rank2)-1)]
            else:
                p1 = rank1.keys()[randint(0,len(rank1)-1)]
            if random()>fav:
                if len(rank2)-1 <= 0:
                    p2 = rank1.keys()[randint(0,len(rank1)-1)]
                else:
                    p2 = rank2.keys()[randint(0,len(rank2)-1)]
                #p2 = rank2.keys()[randint(0,len(rank2)-1)]
            else:
                p2 = rank1.keys()[randint(0,len(rank1)-1)]
            if p1 == p2:
                i += 1
                continue
            parents = [p1,p2]
            parents_list.append(parents)
            i += 1
        return parents_list
    '''

    def parent_selection(self,rank1,rank2,fav,parents_pair,population):
        parents_list = []
        if parents_pair <=0:
            parents_pair = 1
        i = 0
        while(i<parents_pair):
            #print "population",population
            if len(population.keys()) < 2:
                break
            p1 = population.keys()[randint(0,len(population)-1)]
            #print "p1",p1
            del population[p1]
            p2 = population.keys()[randint(0,len(population)-1)]
            #print "p2",p2
            del population[p2]
            parents = [p1,p2]
            parents_list.append(parents)
            i += 1
        return parents_list


    def init_population(self,win_size,temp_job_info_list,not_fes_list):
        temp_population = {}
        temp_list = ['0']*win_size
        for i in range(len(temp_list)):
            temp_temp_list = copy.deepcopy(temp_list)
            temp_temp_list[i] = '1'
            temp_str = ''.join(temp_temp_list)
            d = self.compute_fitness_value(temp_str,temp_job_info_list)
            #if self.is_fesible(d):
            if len(temp_list) > 25:
	            random_chance = uniform(0, 1)
	            if random_chance > 25.0/len(temp_list):
	            	continue
            temp_population[temp_str] = copy.deepcopy(d)
            temp_population[temp_str]['age'] = 0
        popluation_size = int(math.ceil(2**win_size/50))
        if popluation_size < 10:
            popluation_size = 10
        if 2**win_size < 10:
            popluation_size = 2**win_size
        elif popluation_size > 25:
        	popluation_size = 25

        if popluation_size > len(temp_population):
        	temp_popluation_size = popluation_size - len(temp_population)
        else:
        	temp_popluation_size = popluation_size

        start_time =time.time()
        i = 0
        #j = 0
        while(i < temp_popluation_size):
            ri = randint(0,2**win_size-1)
            form = "{0:0"+str(win_size)+"b}"
            temp_index = form.format(ri)
            if temp_index in temp_population.keys():
                continue
            if temp_index in not_fes_list:
                continue
            d = self.compute_fitness_value(temp_index,temp_job_info_list)
            if not self.is_fesible(d):
                not_fes_list.append(temp_index)
                i += 1
                continue

            temp_population[temp_index] = copy.deepcopy(d)
            temp_population[temp_index]['age'] = 0
            #temp_population[temp_index] = {"util":util,"ipower":ipower,"ran_util":ran_util,"age":0}
            i += 1
        self.debug.debug(".....popluation_size :"+' '+str(popluation_size)+' '+str(win_size),5) 
        self.debug.debug(".....popluation_size_iteration :"+' '+str(time.time()-start_time),5) 
        return temp_population,not_fes_list,popluation_size


    def get_pareto_front(self,population):
        rank1 = {}
        rank2 = {}
        #print('population',population)
        for p in population.keys():
            flag = True
            for c in population.keys():
                if p == c:
                    continue

                disturb = False
                for key in population[p].keys():
                    if key != 'age':
                        if not isinstance(population[p][key], list):
                            if population[p][key] > population[c][key]:
                                disturb = True
                                break
                        else:
                            #list_flag = False
                            for x,y in zip(population[p][key],population[c][key]):
                                if x > y:
                                    disturb = True
                                    #list_flag = True
                                    break
                            if disturb:
                                break

                if not disturb:
                    rank2[p] = population[p]
                    flag = False

                '''
                if (population[p]["util"] <= population[c]["util"] and population[p]["wasted_BB_time"] < population[c]["wasted_BB_time"]) or\
                (population[p]["util"] < population[c]["util"] and population[p]["wasted_BB_time"] <= population[c]["wasted_BB_time"]):
                    rank2[p] = population[p]
                    flag = False
                    break
                '''
            if flag:
                rank1[p] = population[p]
        return rank1, rank2

    def is_fesible(self,d):
        if 'util' in d:
            if d['util'] > 1:
                return False
        if 'ran_util' in d:
            for r_temp in d['ran_util']:
                if r_temp > 1:
                    return False
        return True

    def compute_fitness_value(self,index,temp_job_info_list):
        i = 0
        temp_ran = [0]*len(temp_job_info_list[i]['reqRan'])
        temp_proc = 0
        #wasted_BB_time = 0
        while(i < len(temp_job_info_list)):
            if index[i] == '1':
                temp_proc += temp_job_info_list[i]['usedProc']
                for x in range(len(temp_ran)):
                    temp_ran[x] += temp_job_info_list[i]['reqRan'][x]
                #temp_ran += temp_job_info_list[i]['reqRan']
            i += 1
        util = (self.module['node'].get_tot()-self.module['node'].get_avail()+temp_proc)/float(self.module['node'].get_tot())
        ran_util = []
        tot_ran_vol_list = self.module['node'].get_ran_vol_tot()
        avail_ran_vol_list = self.module['node'].get_ran_avail()
        for x in range(len(tot_ran_vol_list)):
            ran_expected_used_vol = float(tot_ran_vol_list[x]-avail_ran_vol_list[x]+temp_ran[x])
            ran_util.append(ran_expected_used_vol/tot_ran_vol_list[x])
        d = dict(); 
        d['util'] = util
        d['ran_util'] = ran_util
        return d
    '''
    def compute_fitness_value(self,index,temp_job_info_list):
        i = 0
        temp_ran = 0
        temp_proc = 0
        while(i < len(temp_job_info_list)):
            if index[i] == '1':
                temp_ran += temp_job_info_list[i]['reqRan']
                temp_proc += temp_job_info_list[i]['usedProc']
            i += 1
        util = (self.module['node'].get_tot()-self.module['node'].get_avail()+temp_proc)/float(self.module['node'].get_tot())
        ran_expected_used_vol = float(self.module['node'].get_ran_vol_tot()-self.module['node'].get_ran_avail()+temp_ran)
        ran_util = ran_expected_used_vol/self.module['node'].get_ran_vol_tot()
        ipower = 1/(self.module['node'].get_xpd_idle_power()*self.module['node'].get_xpd_num()+self.module['node'].get_xpd_active_extra_power()*math.ceil(ran_expected_used_vol*self.module['node'].get_xpd_num()/self.module['node'].get_ran_vol_tot()))
        #ipower = 1/(self.get_xpd_idle_power()+self.get_xpd_active_extra_power()*math.ceil((self.module['node'].get_ran_vol_tot()-self.module['node'].get_ran_avail())/self.module['node'].get_ran_vol_tot()))
        #util = (self.module['node'].get_tot()-self.module['node'].get_avail())/self.module['node'].get_tot()
        #ipower = 1/(self.get_xpd_idle_power()+self.get_xpd_active_extra_power()*math.ceil((self.module['node'].get_ran_vol_tot()-self.module['node'].get_ran_avail())/self.module['node'].get_ran_vol_tot()))
        return util,ipower,ran_util
     '''
    ###################
    
    def start_window(self, temp_wait_B):
        #self.debug.debug("# "+self.myInfo+" -- start_window",5) 
        win_size = self.module['win'].window_size()
        #win_size = 5
        
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
             "node":temp_job['reqProc'],"run":temp_job['run'],"score":temp_job['score'],"reqRan":temp_job['reqRan']})
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

        ran_util_list = []
        tot_ran_vol_list = self.module['node'].get_ran_vol_tot()
        avail_ran_vol_list = self.module['node'].get_ran_avail()
        for x in range(len(tot_ran_vol_list)):
            ran_used_vol = float(tot_ran_vol_list[x]-avail_ran_vol_list[x])
            ran_util_list.append(ran_used_vol/tot_ran_vol_list[x])
        
        self.module['info'].info_collect(time=self.currentTime, event=event_code,\
         uti=(self.module['node'].get_tot()-self.module['node'].get_idle())*1.0/self.module['node'].get_tot(),\
         waitNum=len(self.module['job'].wait_list()), waitSize=self.module['job'].wait_size(), inter=temp_inter,\
         ran_uti=ran_util_list
         )
        self.print_sys_info(self.module['info'].get_info(self.module['info'].get_len()-1))
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
        self.module['output'].print_result(self.module['job'])
        #self.module['output'].print_avg_distance(self.avg_distance_list)
        #self.module['output'].print_util_list(self.util_list)
        #self.module['output'].print_time_list(self.time_list)
        
