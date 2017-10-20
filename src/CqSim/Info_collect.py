from datetime import datetime
import time
from datetime import datetime

__metaclass__ = type
class Info_collect:
    def __init__(self, avg_inter = None, debug = None):
        self.myInfo = "Info Collect"
        self.avg_inter_in = avg_inter
        self.debug = debug
        self.sys_info = []
        self.current_index=-1
        self.start_date = datetime.now()
        self.reset_avg_interval()
        self.show_module_info()
        
        self.eventType={}
        self.eventType['monitor'] = 'C'
        self.eventType['submit'] = 'Q'
        self.eventType['start'] = 'S'
        self.eventType['end'] = 'E'
        
        self.reset_info_data()
        self.add_info_data('inter',None,self.inter_m)
        self.add_info_data('ave_uti',self.ave_uti_j,self.ave_uti_m)
        self.add_info_data('slowdown',self.slowdown_j,self.slowdown_m)
        self.add_info_data('waittime_e',self.waittime_e_j,self.waittime_e_m)
        self.add_info_data('waittime_s',self.waittime_s_j,self.waittime_s_m)
        self.add_info_data('queue_depth',self.queue_depth_j,self.queue_depth_m)
        self.add_info_data('job_start',self.start_j,self.start_m)
        self.add_info_data('job_end',self.end_j,self.end_m)
        self.add_info_data('job_submit',self.submit_j,self.submit_m)
        
    def reset(self, avg_inter = None, debug = None):
        #self.debug.debug("* "+self.myInfo+" -- reset",5)
        if debug:
            self.debug = debug
        if avg_inter:
            self.avg_inter_in = avg_inter
        self.current_index=0
        self.last_time=0
        self.sys_info = []
        self.reset_avg_interval()     
    
    def show_module_info (self):
        #self.debug.line(1," ")
        self.debug.debug("-- "+self.myInfo,1)
        
            
    def inter_m(self):
        self.overall_info['inter'][0] = self.temp_info['time']
        temp_result = self.overall_info['inter'][0] - self.overall_info['inter'][1]
        self.overall_info['inter'][1] = self.overall_info['inter'][0]
        return temp_result 
    
    def submit_j(self):
        if (self.temp_info['event'] == self.eventType['submit']):
            self.overall_info['job_submit'][0] += 1
        return self.overall_info['job_submit'][0]
    
    def submit_m(self):
        temp_result = self.overall_info['job_submit'][0] - self.overall_info['job_submit'][1]
        self.overall_info['job_submit'][1] = self.overall_info['job_submit'][0]
        return temp_result 
    
    def start_j(self):
        if (self.temp_info['event'] == self.eventType['start']):
            self.overall_info['job_start'][0] += 1
        return self.overall_info['job_start'][0]
    
    def start_m(self):
        temp_result = self.overall_info['job_start'][0] - self.overall_info['job_start'][1]
        #self.debug.debug("   "+str(self.overall_info['job_start'][0])+"   "+str(self.overall_info['job_start'][1]),1) 
        self.overall_info['job_start'][1] = self.overall_info['job_start'][0]
        return temp_result 
    
    def end_j(self):
        if (self.temp_info['event'] == self.eventType['end']):
            self.overall_info['job_end'][0] += 1
        return self.overall_info['job_end'][0]
    
    def end_m(self):
        temp_result = self.overall_info['job_end'][0] - self.overall_info['job_end'][1]
        self.overall_info['job_end'][1] = self.overall_info['job_end'][0]
        return temp_result 
    
    def ave_uti_j(self):
        try:
            if (self.last_time<self.temp_info['time']):
                self.overall_info['ave_uti'][0] += (self.temp_info['time']-self.last_time) * self.sys_info[self.current_index]['uti']        
                self.last_time = self.temp_info['time']
            
            if (self.temp_info['time']-self.sys_info[0]['time']>0 ):
                temp_result = self.overall_info['ave_uti'][0]*1.0/(self.temp_info['time']-self.sys_info[0]['time'])
            else:
                temp_result = 0
        except:
            self.overall_info['ave_uti'][0] = 0.0
            temp_result = 0
        
        return temp_result 
    
    def ave_uti_m(self):
        temp_time2 = self.temp_info['inter']
        if temp_time2>0:
            temp_result = (self.overall_info['ave_uti'][0] - self.overall_info['ave_uti'][1])/temp_time2
        else:
            temp_result = 0
        self.overall_info['ave_uti'][1] = self.overall_info['ave_uti'][0]
        
        return temp_result 
    
    def slowdown_j(self):
        temp_result = -1
        if (self.temp_info['event'] == self.eventType['end']):
            temp_result = (self.current_para['end']-self.current_para['submit'])*1.0/self.current_para['run']
            self.overall_info['slowdown'][0] += temp_result
        return temp_result
    
    def slowdown_m(self):
        temp_job_num = (self.overall_info['job_end'][0] - self.overall_info['job_end'][1])
        if temp_job_num>0:
            temp_result = (self.overall_info['slowdown'][0] - self.overall_info['slowdown'][1])/temp_job_num
        else:
            temp_result = 0
        self.overall_info['slowdown'][1] = self.overall_info['slowdown'][0]
        return temp_result 
    
    def waittime_e_j(self):
        temp_result = -1
        if (self.temp_info['event'] == self.eventType['end']):
            temp_result = self.current_para['start']-self.current_para['submit']
            self.overall_info['waittime_e'][0] += temp_result
        return temp_result
    
    def waittime_e_m(self):
        temp_job_num = (self.overall_info['job_end'][0] - self.overall_info['job_end'][1])
        if temp_job_num>0:
            temp_result = (self.overall_info['waittime_e'][0] - self.overall_info['waittime_e'][1])/temp_job_num
        else:
            temp_result = 0
        self.overall_info['waittime_e'][1] = self.overall_info['waittime_e'][0]
        return temp_result 
    
    def waittime_s_j(self):
        temp_result = -1
        if (self.temp_info['event'] == self.eventType['start']):
            temp_result = self.current_para['start']-self.current_para['submit']
            self.overall_info['waittime_s'][0] += temp_result
        return temp_result
    
    def waittime_s_m(self):
        temp_job_num = (self.overall_info['job_start'][0] - self.overall_info['job_start'][1])
        if temp_job_num>0:
            temp_result = (self.overall_info['waittime_s'][0] - self.overall_info['waittime_s'][1])/temp_job_num
        else:
            temp_result = 0
        self.overall_info['waittime_s'][1] = self.overall_info['waittime_s'][0]
        return temp_result 

    def queue_depth_j(self):
        temp_result = -1
        if (self.temp_info['event'] == self.eventType['submit']):
            self.overall_info['queue_depth'][0] -= (self.temp_info['time']-self.overall_info['inter'][1])
        elif (self.temp_info['event'] == self.eventType['start']):
            self.overall_info['queue_depth'][0] += (self.temp_info['time']-self.overall_info['inter'][1])
        return None
    
    def queue_depth_m(self):         
        temp_time2 = self.temp_info['inter']
        temp_job_wait = self.overall_info['job_submit'][0] - self.overall_info['job_start'][0]
        self.overall_info['queue_depth'][0] += temp_time2*temp_job_wait
        
        if (temp_time2>0):
            temp_result = (self.overall_info['queue_depth'][0] - self.overall_info['queue_depth'][1])*1.0/temp_time2*1800
        else:
            temp_result = 0
        self.overall_info['queue_depth'][1] = self.overall_info['queue_depth'][0]
        #self.debug.debug("   "+str(temp_time2),1) 
        return temp_result 
            
    
    def reset_info_data (self):
        self.info_data=[]
        self.overall_info={}
        self.data_num = 0
        self.last_time=0
        
    def add_info_data (self, data_name, j_func = None, m_func = None):
        self.info_data.append({'name':data_name,'j_func':j_func,'m_func':m_func})
        self.overall_info[data_name] = [0,0] 
        self.data_num += 1
    
    def reset_start_date (self,date):
        self.start_date = date       
        
    def info_collect(self, time, event, uti, extend = None, current_para = None):
        #self.debug.debug("* "+self.myInfo+" -- info_collect",5)
        self.current_para=current_para
        event_date = self.start_date.strftime("%m/%d/%Y %H:%M:%S")
        self.temp_info = {'date': event_date, 'time': time, 'event': event, 'uti': uti, 'extend': extend, 'tot_avg_uti': 0.0, 'avg_uti':[]}
            
        self.info_analysis(self.temp_info['event'])
        self.temp_info['tot_uti'] = self.overall_info['ave_uti'][0]
        ##############################################
        self.sys_info.append(self.temp_info)
        self.current_index += 1
        self.calculate_avg_uti()
        #if (event == 'C'):
        #    self.debug.debug("   "+str(self.temp_info),1) 
        
    def info_analysis(self,event):
        #self.debug.debug("* "+self.myInfo+" -- info_analysis",5)
        i = 0
        if (event == self.eventType['submit'] or event == self.eventType['start'] or event == self.eventType['end']):
            while (i<self.data_num):
                data_item = self.info_data[i]
                if data_item['j_func'] != None :
                    self.temp_info[data_item['name']] = data_item['j_func']()
                i += 1
        elif (event == self.eventType['monitor']):
            while (i<self.data_num):
                data_item = self.info_data[i]
                if data_item['m_func'] != None :
                    self.temp_info[data_item['name']] = data_item['m_func']()
                i += 1
        #self.debug.debug("   "+str(self.temp_info),1) 
        return 1
    
    def get_info(self, index):
        #self.debug.debug("* "+self.myInfo+" -- get_info",6)
        if index>=len(self.sys_info):
            return None
        return self.sys_info[index]
    
    def get_len(self):
        #self.debug.debug("* "+self.myInfo+" -- get_len",6)
        return len(self.sys_info)
    
    def get_current_index(self):
        #self.debug.debug("* "+self.myInfo+" -- get_len",6)
        return self.current_index
    
    def calculate_avg_uti (self):
        i = 0
        while (i < len(self.avg_inter)):
            self.sys_info[len(self.sys_info)-1]['avg_uti'].append(-1)
            i += 1
        
        i = len(self.sys_info) - 2
        j = 0
        temp_num = len(self.order_seq)
        current_time = self.sys_info[len(self.sys_info)-1]['time']
        temp_time = current_time
        temp_uti = 0
        while (i>=0 and j<temp_num):
            if (current_time-self.sys_info[i]['time']>=self.avg_inter[self.order_seq[j]]):
                temp_uti_B = temp_uti +(self.avg_inter[self.order_seq[j]] - (current_time - temp_time)) * self.sys_info[i]['uti']
                self.sys_info[len(self.sys_info)-1]['avg_uti'][self.order_seq[j]] = temp_uti_B/self.avg_inter[self.order_seq[j]]
                #self.debug.debug("    {"+str(self.order_seq[j])+":"+str(self.avg_inter[self.order_seq[j]])+"}:"+str(temp_uti_B),2)
                j += 1
            elif (i > 0):
                temp_uti += (temp_time - self.sys_info[i]['time']) * self.sys_info[i]['uti']
                temp_time = self.sys_info[i]['time']  
                i -= 1
            else:
                temp_uti += (temp_time - self.sys_info[i]['time']) * self.sys_info[i]['uti']
                temp_interval = current_time-self.sys_info[i]['time']
                while (j<temp_num):
                    if temp_interval == 0:
                        self.sys_info[len(self.sys_info)-1]['avg_uti'][self.order_seq[j]] = 0
                    else:
                        self.sys_info[len(self.sys_info)-1]['avg_uti'][self.order_seq[j]] = temp_uti/temp_interval
                    #self.debug.debug("    x{"+str(self.order_seq[j])+":"+str(self.avg_uti[self.order_seq[j]])+"}:"+str(temp_uti),2)
                    j += 1
        
    def reset_avg_interval (self):
        self.total_uti = 0
        self.order_seq = []
        self.avg_inter = []
        if self.avg_inter_in != None:
            for avg_inter in self.avg_inter_in:
                self.avg_inter.append(float(avg_inter))
            
    def reorder_avg_interval (self):
        self.order_seq = []
        i = 0
        uti_len = len(self.avg_inter)
        while (i<uti_len):
            j = 0
            while (j<len(self.order_seq)):
                if (self.avg_inter[i]<self.avg_inter[self.order_seq[j]]):
                    break
                j += 1
            if (j>=len(self.order_seq)):
                self.order_seq.append(i)
            else:
                self.order_seq.insert(j,i)  
            i += 1
    