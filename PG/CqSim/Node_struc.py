from datetime import datetime
import time
import re

__metaclass__ = type

class Node_struc:
    def __init__(self, debug=None):
        self.myInfo = "Node Structure"
        self.debug = debug
        self.nodeStruc = []
        self.job_list = []
        self.predict_node = []
        self.predict_job = []
        self.tot = -1
        self.idle = -1
        self.avail = -1
        
        self.debug.line(4," ")
        self.debug.line(4,"#")
        self.debug.debug("# "+self.myInfo,1)
        self.debug.line(4,"#")
        
    def reset(self, debug=None):
        #self.debug.debug("* "+self.myInfo+" -- reset",5)
        self.debug = debug
        self.nodeStruc = []
        self.job_list = []
        self.predict_node = []
        self.tot = -1
        self.idle = -1
        self.avail = -1
        
    def read_list(self,source_str):
        #self.debug.debug("* "+self.myInfo+" -- read_list",5)
        result_list=[]
        regex_str = "[\[,]([^,\[\]]*)"
        result_list=re.findall(regex_str,source_str)
        for item in result_list:
            item=int(item)
        return result_list
    
    def import_node_file(self, node_file):
        #self.debug.debug("* "+self.myInfo+" -- import_node_file",5)
        regex_str = "([^;\\n]*)[;\\n]"
        nodeFile = open(node_file,'r')
        self.nodeStruc = []
        
        i = 0
        while (1):
            tempStr = nodeFile.readline()
            if not tempStr :    # break when no more line
                break
            temp_dataList=re.findall(regex_str,tempStr)
                
            self.debug.debug("  node["+str(i)+"]: "+str(temp_dataList),4)
            tempInfo = {"id": int(temp_dataList[0]), \
                          "location": self.read_list(temp_dataList[1]), \
                          "group": int(temp_dataList[2]), \
                          "state": int(temp_dataList[3]), \
                          "proc": int(temp_dataList[4]), \
                          "start": -1, \
                          "end": -1, \
                          "extend": None}
            self.nodeStruc.append(tempInfo)
            i += 1
        nodeFile.close()
        self.tot = len(self.nodeStruc)
        self.idle = self.tot
        self.avail = self.tot
        self.debug.debug("  Tot:"+str(self.tot)+" Idle:"+str(self.idle)+" Avail:"+str(self.avail)+" ",4)
        #print('self.nodeStruc',self.nodeStruc)
        return
        
    def import_node_config (self, config_file):
        #self.debug.debug("* "+self.myInfo+" -- import_node_config",5)
        regex_str = "([^=\\n]*)[=\\n]"
        nodeFile = open(config_file,'r')
        config_data={}
                
        self.debug.line(4)
        while (1):
            tempStr = nodeFile.readline()
            if not tempStr :    # break when no more line
                break
            temp_dataList=re.findall(regex_str,tempStr)
            config_data[temp_dataList[0]]=temp_dataList[1]
            self.debug.debug(str(temp_dataList[0])+": "+str(temp_dataList[1]),4)
        self.debug.line(4)
        nodeFile.close()
        
    def import_node_data(self, node_data):
        #self.debug.debug("* "+self.myInfo+" -- import_node_data",5)
        self.nodeStruc = []
        
        temp_len = len(node_data)
        i=0
        while (i<temp_len):
            temp_dataList = node_data[i]
                
            tempInfo = {"id": temp_dataList[0], \
                          "location": temp_dataList[1], \
                          "group": temp_dataList[2], \
                          "state": temp_dataList[3], \
                          "proc": temp_dataList[4], \
                          "start": -1, \
                          "end": -1, \
                          "extend": None}
            self.nodeStruc.append(tempInfo)
            i += 1
        self.tot = len(self.nodeStruc)
        self.idle = self.tot
        self.avail = self.tot
        
    def is_available(self, proc_num):
        #self.debug.debug("* "+self.myInfo+" -- is_available",6)
        result = 0
        if self.avail >= proc_num:
            result = 1
        self.debug.debug("[Avail Check] "+str(result),6)
        return result
        
    def get_tot(self):
        #self.debug.debug("* "+self.myInfo+" -- get_tot",6)
        return self.tot
        
    def get_idle(self):
        #self.debug.debug("* "+self.myInfo+" -- get_idle",6)
        return self.idle
        
    def get_avail(self):
        #self.debug.debug("* "+self.myInfo+" -- get_avail",6)
        return self.avail

    def get_nodeStruc(self):
        return self.nodeStruc
        
    def node_allocate(self, proc_num, job_index, start, end):
        #self.debug.debug("* "+self.myInfo+" -- node_allocate",5)
        if self.is_available(proc_num) == 0:
            return 0
        i = 0
        for node in self.nodeStruc:
            if node['state'] <0:
                node['state'] = job_index
                node['start'] = start
                node['end'] = end
                i += 1
            #self.debug.debug("  yyy: "+str(node['state'])+"   "+str(job_index),4)
            if (i>=proc_num):
                break
        self.idle -= proc_num
        self.avail = self.idle
        temp_job_info = {'job':job_index, 'end': end, 'node': proc_num}
        j = 0
        is_done = 0
        temp_num = len(self.job_list)
        while (j<temp_num):
            if (temp_job_info['end']<self.job_list[j]['end']):
                self.job_list.insert(j,temp_job_info)
                is_done = 1
            j += 1
            
        if (is_done == 0):
            self.job_list.append(temp_job_info)
            
        self.debug.debug("  Allocate"+"["+str(job_index)+"]"+" Req:"+str(proc_num)+" Avail:"+str(self.avail)+" ",4)
        return 1
        
    def node_release(self, job_index, end):
        #self.debug.debug("* "+self.myInfo+" -- node_release",5)
        i = 0
        for node in self.nodeStruc:
            #self.debug.debug("  xxx: "+str(node['state'])+"   "+str(job_index),4)
            if node['state'] == job_index:
                node['state'] = -1
                node['start'] = -1
                node['end'] = -1
                i += 1
        if i <= 0:
            self.debug.debug("  Release Fail!",4)
            return 0
        self.idle += i
        self.avail = self.idle
        j = 0
        temp_num = len(self.job_list)
        while (j<temp_num):
            if (job_index==self.job_list[j]['job']):
                break
            j += 1
        self.job_list.pop(j)
        self.debug.debug("  Release"+"["+str(job_index)+"]"+" Req:"+str(i)+" Avail:"+str(self.avail)+" ",4)
        return 1
        
    def pre_avail(self, proc_num, start, end = None):
        #self.debug.debug("* "+self.myInfo+" -- pre_avail",6)
        #self.debug.debug("pre avail check: "+str(proc_num)+" (" +str(start)+";"+str(end)+")",6)
        if not end or end < start:
            end = start
             
        i = 0
        temp_job_num = len(self.predict_node)
        while (i < temp_job_num):
            if (self.predict_node[i]['time']>=start and self.predict_node[i]['time']<end):
                if (proc_num>self.predict_node[i]['avail']):
                    return 0
            i += 1
        return 1
        
    def reserve(self, proc_num, job_index, time, start = None, index = -1 ):
        #self.debug.debug("* "+self.myInfo+" -- reserve",5)
            
        temp_max = len(self.predict_node)
        if (start):
            if (self.pre_avail(proc_num,start,start+time)==0):
                return -1
        else:
            i = 0
            j = 0
            if (index >= 0 and index < temp_max):
                i = index
            elif(index >= temp_max):
                return -1
            
            while (i<temp_max): 
                if (proc_num<=self.predict_node[i]['avail']):
                    j = self.find_res_place(proc_num,i,time)
                    if (j == -1):
                        start = self.predict_node[i]['time']
                        break
                    else:
                        i = j + 1
                else:
                    i += 1

        end = start + time
        j = i
        
        '''
        # Insert the start time item. Useless becasue no new item should be insert.
        i = 0
        j = -1
        while (i < temp_max):
            if (self.predict_node[i]['time']<start):
                i += 1
            elif (self.predict_node[i]['time']==start):
                j = i
                break
            else:
                temp_list = []
                k = 0
                while k< self.tot:
                    temp_list.append(self.predict_node[i-1]['node'][k])
                    k += 1
                self.predict_node.insert(i,{'time':start, 'node':temp_list,\
                                    'idle':self.predict_node[i-1]['idle'], 'avail':self.predict_node[i-1]['avail']})
                j = i
                break
        '''    
        
        is_done = 0
        start_index = j
        while (j < temp_max):
            if (self.predict_node[j]['time']<end):
                k = 0
                n = 0
                while k< self.tot and n < proc_num:
                    if (self.predict_node[j]['node'][k] == -1):
                        self.predict_node[j]['node'][k] = job_index
                        self.predict_node[j]['idle'] -= 1
                        self.predict_node[j]['avail'] = self.predict_node[j]['idle']
                        n += 1
                    k += 1
                j += 1
            elif (self.predict_node[j]['time']==end):
                is_done = 1
                break
            else:
                temp_list = []
                k = 0
                while k< self.tot:
                    temp_list.append(self.predict_node[j-1]['node'][k])
                    k += 1
                self.predict_node.insert(j,{'time':end, 'node':temp_list,\
                                    'idle':self.predict_node[j-1]['idle'], 'avail':self.predict_node[j-1]['avail']})
                k = 0
                n = 0
                #self.debug.debug("xx   "+str(proc_num),4)
                while k< self.tot and n < proc_num:
                    if (self.predict_node[j]['node'][k] == job_index):
                        self.predict_node[j]['node'][k] = -1
                        self.predict_node[j]['idle'] += 1
                        self.predict_node[j]['avail'] = self.predict_node[j]['idle']
                        n += 1
                    k += 1
                is_done = 1
                
                #self.debug.debug("xx   "+str(n)+"   "+str(k),4)
                break
            
        temp_list = []
        if (is_done != 1):
            k = 0
            while k< self.tot:
                temp_list.append(-1)
                k += 1
            self.predict_node.append({'time':end, 'node':temp_list,\
                                'idle':self.tot, 'avail':self.tot})
                
        self.predict_job.append({'job':job_index, 'start':start, 'end':end})
        '''
        i = 0
        self.debug.line(4,'.')
        temp_num = len(self.predict_node)
        self.debug.debug(temp_num,4)
        while (i<temp_num):
            self.debug.debug("O "+str(self.predict_node[i]),4)
            i += 1
        self.debug.line(4,'.')
        ''' 
        return start_index
     
    def pre_delete(self, proc_num, job_index):
        #self.debug.debug("* "+self.myInfo+" -- pre_delete",5)
        return 1
        
    def pre_modify(self, proc_num, start, end, job_index):  
        #self.debug.debug("* "+self.myInfo+" -- pre_modify",5)  
        return 1
        
    def pre_get_last(self):
        #self.debug.debug("* "+self.myInfo+" -- pre_get_last",6)
        pre_info_last= {'start':-1, 'end':-1}
        for temp_job in self.predict_job:
            #self.debug.debug("xxx   "+str(temp_job),4)
            if (temp_job['start']>pre_info_last['start']):
                pre_info_last['start'] = temp_job['start']
            if (temp_job['end']>pre_info_last['end']):
                pre_info_last['end'] = temp_job['end']
        return pre_info_last
        
    def pre_reset(self, time):
        #self.debug.debug("* "+self.myInfo+" -- pre_reset",5)  
        self.predict_node = []
        self.predict_job = []
        temp_list = []
        i = 0
        while i< self.tot:
            temp_list.append(self.nodeStruc[i]['state'])
            i += 1
        self.predict_node.append({'time':time, 'node':temp_list,\
                            'idle':self.idle, 'avail':self.avail})
                            
        temp_job_num = len(self.job_list)
        i = 0
        j = 0
        while i< temp_job_num:
            if (self.predict_node[j]['time']!=self.job_list[i]['end'] or i == 0):
                temp_list = []
                k = 0
                while k< self.tot:
                    temp_list.append(self.predict_node[j]['node'][k])
                    k += 1
                self.predict_node.append({'time':self.job_list[i]['end'], 'node':temp_list,\
                                    'idle':self.predict_node[j]['idle'], 'avail':self.predict_node[j]['avail']})
                j += 1
            k=0
            while k< self.tot:
                if (self.predict_node[j]['node'][k] == self.job_list[i]['job']):
                    self.predict_node[j]['node'][k] = -1
                    self.predict_node[j]['idle'] += 1
                k += 1
            i += 1
            self.predict_node[j]['avail'] = self.predict_node[j]['idle']
        '''
        i = 0
        while i< self.tot:
            if self.nodeStruc[i]['state'] != -1:
                temp_index = get_pre_index(temp_time = self.nodeStruc[i]['end'])
                self.predict_node[temp_index]['node'][i] = self.nodeStruc[i]['state']
            i += 1
        '''
        return 1
        
    
    def find_res_place(self, proc_num, index, time):
        self.debug.debug("* "+self.myInfo+" -- find_res_place",5)  
        if index>=len(self.predict_node):
            index = len(self.predict_node) - 1
             
        i = index
        end = self.predict_node[index]['time']+time
        temp_node_num = len(self.predict_node)
        
        while (i < temp_node_num):
            if (self.predict_node[i]['time']<end):
                if (proc_num>self.predict_node[i]['avail']):
                    #print "xxxxx   ",temp_node_num,proc_num,self.predict_node[i]
                    return i
            i += 1
        return -1