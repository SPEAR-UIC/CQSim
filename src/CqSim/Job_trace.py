from datetime import datetime
import time
import re

__metaclass__ = type

class Job_trace:
    def __init__(self, start=-1, num=-1, anchor=-1, density=1.0, debug=None):
        self.myInfo = "Job Trace"
        self.start = start
        self.start_offset_A = 0.0
        self.start_offset_B = 0.0
        self.start_date = ""
        self.anchor = anchor
        self.read_num = num
        self.density = density
        self.debug = debug
        self.jobTrace=[]

        self.debug.line(4," ")
        self.debug.line(4,"#")
        self.debug.debug("# "+self.myInfo,1)
        self.debug.line(4,"#")

        self.reset_data()

    def reset(self, start=None, num=None, anchor=None, density=None, debug=None):
        #self.debug.debug("* "+self.myInfo+" -- reset",5)
        if start:
            self.anchor = start
            self.start_offset_A = 0.0
            self.start_offset_B = 0.0
        if num:
            self.read_num = num
        if anchor:
            self.anchor = anchor
        if density:
            self.density = density
        if debug:
            self.debug = debug
        self.jobTrace=[]
        self.reset_data()

    def reset_data(self):
        #self.debug.debug("* "+self.myInfo+" -- reset_data",5)
        self.job_wait_size = 0
        self.job_submit_list=[]
        self.job_wait_list=[]
        self.job_run_list=[]
        self.job_done_list=[]
        #self.bb_wait_list=[]
        #self.bb_wait_size = 0
        #self.bb_stage_in_list=[]
        #self.bb_stage_out_list=[]


    def import_job_file (self, job_file, module_filter_node):
        #self.debug.debug("* "+self.myInfo+" -- import_job_file",5)
        temp_start=self.start
        regex_str = "([^;\\n]*)[;\\n]"
        jobFile = open(job_file,'r')
        min_sub = -1
        self.jobTrace=[]
        self.reset_data()

        self.debug.line(4)
        i = 0
        j = 0
        while (i<self.read_num or self.read_num<=0):
            tempStr = jobFile.readline()
            #print(tempStr)
            if not tempStr :    # break when no more line
                break
            if (j>=self.anchor):
                temp_dataList=re.findall(regex_str,tempStr)
                #print(tempStr,temp_dataList)

                if (min_sub<0):
                    min_sub=float(temp_dataList[1])
                    if (temp_start < 0):
                        temp_start = min_sub
                    self.start_offset_B = min_sub-temp_start

                tempInfo = {'id':int(temp_dataList[0]),\
                            'submit':self.density*(float(temp_dataList[1])-min_sub)+temp_start,\
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
                            'reqRan':[],\
                            'start':-1,\
                            'end':-1,\
                            'score':0,\
                            'state':0,\
                            'happy':-1,\
                            'estStart':-1}
                x = 18
                while x < len(temp_dataList):
                    #print('temp_dataList',len(temp_dataList),temp_dataList[i])
                    tempInfo['reqRan'].append(int(temp_dataList[x]))
                    x += 1
                #int(temp_dataList[18])
                #print('tempInfo[reqRan]',tempInfo['reqRan'],i,j)
                tot_num_proc = 0
                tot_BurstBuffer = []
                for con_data in module_filter_node.config_data:
                    if con_data['name'] == "MaxProcs":
                        tot_num_proc = int(con_data['value'])
                    elif con_data['name'] == "BurstBuffer":
                        tot_BurstBuffer = [int(x) for x in con_data['value'].split(',')]
                if tempInfo['reqProc']<0 or tempInfo['reqProc']>tot_num_proc:
                    #print(tot_BurstBuffer,tempInfo['reqRan'])
                    #i += 1
                    continue

                flag = False
                for x, y in zip(tot_BurstBuffer,tempInfo['reqRan']):
                    #print(x,y)
                    if x < y:
                        flag = True
                if flag:
                    continue

                self.jobTrace.append(tempInfo)
                self.job_submit_list.append(i)
                self.debug.debug(temp_dataList,4)
                #self.debug.debug("* "+str(tempInfo),4)
                #print('i',i)
                i += 1
            j += 1

        self.debug.line(4)
        jobFile.close()

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


    '''
    def import_job_data (self, job_data):
        #self.debug.debug("* "+self.myInfo+" -- import_job_data",5)
        temp_start=self.anchor
        min_sub = -1
        self.jobTrace=[]
        self.reset_list()
        data_len = len(job_data)

        i = 0
        j = 0
        while ((i < data_len) and (i<self.read_num or self.read_num<=0)):
            if (j>=self.anchor):
                temp_dataList=job_data[i]

                if (min_sub<0):
                    min_sub=float(temp_dataList[1])
                    if (temp_start < 0):
                        temp_start = min_sub

                tempInfo = {'id':int(temp_dataList[0]),\
                            'submit':self.density*(float(temp_dataList[1])-min_sub)+temp_start,\
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
                            'reqRan':int(temp_dataList[18]),\
                            'start':-1,\
                            'end':-1,\
                            'score':0,\
                            'state':0,\
                            'happy':-1,\
                            'estStart':-1}
                self.jobTrace=[].append(tempInfo)
                self.job_submit_list.append(i)
                i += 1
            j += 1
        return
    '''
    
    def submit_list (self):
        #self.debug.debug("* "+self.myInfo+" -- submit_list",6)
        return self.job_submit_list

    def wait_list (self):
        #self.debug.debug("* "+self.myInfo+" -- wait_list",6)
        return self.job_wait_list

    def run_list (self):
        #self.debug.debug("* "+self.myInfo+" -- run_list",6)
        return self.job_run_list

    def done_list (self):
        #self.debug.debug("* "+self.myInfo+" -- done_list",6)
        return self.job_done_list

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
        self.job_wait_list.sort(self.scoreCmp)
        #self.debug.debug("  Wait:"+str(self.job_wait_list),4)

    def update_wait_list(self, job_wait_list):
        self.job_wait_list = job_wait_list

    def scoreCmp(self,jobIndex_c1,jobIndex_c2):
        return -cmp(self.jobTrace[jobIndex_c1]['score'],self.jobTrace[jobIndex_c2]['score'])

    def job_info (self, job_index = -1):
        #self.debug.debug("* "+self.myInfo+" -- job_info",6)
        if job_index == -1:
            return self.jobTrace
        return self.jobTrace[job_index]

    ###
    '''
    def submit_job_without_stage_in(self,job_index, currentTime, job_score = 0, job_est_start = -1):
        #print 'submit_job_without_stage_in',job_index
        self.jobTrace[job_index]["state"]=1
        self.jobTrace[job_index]["score"]=job_score
        self.jobTrace[job_index]["estStart"]=job_est_start
        self.jobTrace[job_index]['bwait'] = currentTime - self.jobTrace[job_index]['submit']
        self.bb_wait_list.remove(job_index)
        self.bb_wait_size -= self.jobTrace[job_index]["reqRan"]
        self.job_wait_list.append(job_index)
        self.job_wait_size += self.jobTrace[job_index]["reqProc"]
        return 1

    def submit_job_after_stage_in(self,job_index, job_score = 0, job_est_start = -1):
        self.jobTrace[job_index]["state"]=1
        self.jobTrace[job_index]["score"]=job_score
        self.jobTrace[job_index]["estStart"]=job_est_start
        self.bb_stage_in_list.remove(job_index)
        self.job_wait_list.append(job_index)
        self.job_wait_size += self.jobTrace[job_index]["reqProc"]
        return 1


    def job_stage_in_start(self,job_index,time):
        self.jobTrace[job_index]["state"]=12
        self.jobTrace[job_index]['bIstart']=time
        self.jobTrace[job_index]['bwait']=time-self.jobTrace[job_index]['submit']
        self.jobTrace[job_index]['bIend'] = time+self.jobTrace[job_index]['stageInTime']
        self.bb_wait_list.remove(job_index)
        self.bb_stage_in_list.append(job_index)
        self.bb_wait_size -= self.jobTrace[job_index]["reqRan"]
        return 1

    def job_stage_out_start(self,job_index,time):
        self.jobTrace[job_index]["state"]=31
        self.jobTrace[job_index]['bOend'] = time+self.jobTrace[job_index]['stageOutTime']
        self.bb_stage_out_list.append(job_index)
        return 1

    def job_stage_out_end(self,job_index):
        #if self.jobTrace[job_index]['stageOutTime'] > 0:
        self.bb_stage_out_list.remove(job_index)
        self.jobTrace[job_index]["state"]=32
        self.job_done_list.append(job_index)
        temp_job = self.jobTrace[job_index]
        self.debug.debug("[Finish]  "+str(job_index)+" Stage In Wait, Start, End Time: "+str(temp_job["bwait"])+","+str(temp_job["bIstart"])+","+str(temp_job["bIend"])+","+" StartTime: "+str(temp_job["start"])+" EndTime: "+str(temp_job["end"])+" Stage Out End: "+str(temp_job["bOend"]),3)
        return 1
    '''
    ###

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
        #self.debug.debug(" "+"["+str(job_index)+"]"+" Req:"+str(self.jobTrace[job_index]['reqProc'])+" Run:"+str(self.jobTrace[job_index]['run'])+" ",2)
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
        #self.debug.debug(" "+"["+str(job_index)+"]"+" Req:"+str(self.jobTrace[job_index]['reqProc'])+" Run:"+str(self.jobTrace[job_index]['run'])+" ",4)
        self.jobTrace[job_index]["state"]=3
        if  time:
            self.jobTrace[job_index]['end'] = time
        self.job_run_list.remove(job_index)
        self.job_done_list.append(job_index)
        return 1

    def job_fail (self, job_index, time=None):
        #self.debug.debug("* "+self.myInfo+" -- job_fail",5)
        #self.debug.debug(" "+"["+str(job_index)+"]"+" Req:"+str(self.jobTrace[job_index]['reqProc'])+" Run:"+str(self.jobTrace[job_index]['run'])+" ",4)
        self.jobTrace[job_index]["state"]=4
        if  time:
            self.jobTrace[job_index]['end'] = time
        self.job_run_list.remove(job_index)
        self.fail_list.append(job_index)
        return 1

    def job_set_score (self, job_index, job_score):
        #self.debug.debug("* "+self.myInfo+" -- job_set_score",5)
        self.jobTrace[job_index]["score"]=job_score
        return 1
