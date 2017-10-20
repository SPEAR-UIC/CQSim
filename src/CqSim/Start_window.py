import cqsim_path
import re
__metaclass__ = type
class Start_window:
    def __init__(self, mode = 0, ad_mode = 0, node_module = None, info_module = None, debug = None, para_list = [5,0,0], ad_para_list = None):
        self.myInfo = "Start Window"
        self.para={}
        self.para['mode'] = mode
        self.para['ad_mode'] = ad_mode
        self.node_module = node_module
        self.info_module = info_module
        self.debug = debug
        self.para_list = para_list
        self.ad_para_list = ad_para_list
        if ad_para_list:
            self.para['ad_config'] = cqsim_path.path_config+ad_para_list[0]
        else:
            self.para['ad_config'] = None
        #print self.para_list
        if (len(self.para_list)>=1 and int(self.para_list[0]) > 0):
            self.para['win_size'] = int(self.para_list[0])
        else:
            self.para['win_size'] = 1
        if (len(self.para_list)>=2 and int(self.para_list[1]) > 0):
            self.para['check_size'] = int(self.para_list[1])
        else:
            self.para['check_size'] = self.para['win_size']
        if (len(self.para_list)>=3 and int(self.para_list[2]) > 0):
            self.para['max_start_size'] = int(self.para_list[2])
        else:
            self.para['max_start_size'] = self.para['win_size']
        if (len(self.para_list)>=4 and int(self.para_list[3]) > 0):
            self.para['max_win_size'] = int(self.para_list[3])
        else:
            self.para['max_win_size'] = self.para['win_size']
            
        self.temp_check_len = self.para['check_size']
        
        self.current_para = []
        self.seq_list = []
        self.show_module_info()
        
        self.reset_list()
        self.adapt_reset()
        
    def reset (self, mode = None,  ad_mode = None, node_module = None, info_module = None, debug = None, para_list = None, ad_para_list = None):
        #self.debug.debug("* "+self.myInfo+" -- reset",5) 
        if mode:
            self.para['mode'] = mode
        if ad_mode:
            self.para['ad_mode'] =ad_mode
        if node_module:
            self.node_module = node_module
        if info_module:
            self.info_module = info_module
        if debug:
            self.debug = debug
        if para_list:
            self.para_list = para_list
            if (self.para_list[0] and self.para_list[0] > 0):
                self.para['win_size'] = self.para_list[0]
            else:
                self.para['win_size'] = 1
            if (self.para_list[1] and self.para_list[1] > 0):
                self.para['check_size'] = self.para_list[1]
            else:
                self.para['check_size'] = self.para['win_size']
            if (self.para_list[2] and self.para_list[2] > 0):
                self.para['max_start_size'] = self.para_list[2]
            else:
                self.para['max_start_size'] = self.para['win_size']
            if (len(self.para_list)>=4 and int(self.para_list[3]) > 0):
                self.para['max_win_size'] = int(self.para_list[3])
            else:
                self.para['max_win_size'] = self.para['win_size']
        if ad_para_list:
            self.ad_paralist = ad_para_list
            self.para['ad_config'] = cqsim_path.path_config+ad_para_list[0]
            
        self.current_para = []
        self.seq_list = []
        self.reset_list()
        self.adapt_reset()
    
    def show_module_info (self):
        #self.debug.line(1," ")
        self.debug.debug("-- "+self.myInfo,1)   
    
    def start_window (self, wait_job, para_in = None):
        #self.debug.debug("* "+self.myInfo+" -- start_window",5) 
        self.current_para = para_in
        temp_len = len(wait_job)
        self.wait_job = []
        i = 0
        result_b = []
        while (i < self.para['win_size'] and i < temp_len):
            self.wait_job.append(wait_job[i])
            if i>=self.para['check_size']:
                result_b.append(wait_job[i]['index'])
            i += 1
        if i>self.para['check_size']:
            i = self.para['check_size']
        self.temp_check_len = i
        result = self.main()
        result_b[0:0]=result
        return result_b
    
    def main (self):
        #self.debug.debug("* "+self.myInfo+" -- main",5) 
        result = []
        if self.para['mode'] == 1:
            # window
            result = self.window_check()
            #print ">>>>>>>>>>. ",result
        else:
            # no window
            i = 0
            temp_list=[]
            while (i < self.temp_check_len):
                temp_list.append(self.wait_job[i]['index'])
                i += 1
            return temp_list
        return result
    
    def window_size (self):
        #self.debug.debug("* "+self.myInfo+" -- window_size",6) 
        return int(self.para['win_size'])
    
    def check_size (self):
        #self.debug.debug("* "+self.myInfo+" -- check_size",6) 
        return int(self.para['check_size'])
    
    def start_num (self):
        #self.debug.debug("* "+self.myInfo+" -- start_num",6) 
        return int(self.para['max_start_size'])
    
    def reset_list (self):
        #self.debug.debug("* "+self.myInfo+" -- reset_list",5) 
        self.seq_list = []
        self.temp_list=[]
        self.wait_job = []
        temp_seq=[]
        i = 0
        ele = []
        while (i<self.para['max_win_size']):
            ele.append(i)
            self.temp_list.append(-1)
            i += 1
        self.build_seq_list(self.para['max_win_size'], ele, self.para['max_win_size']-1)

    def build_seq_list(self, seq_len, ele_pool, temp_index):
        #self.debug.debug("* "+self.myInfo+" -- build_seq_list",6) 
        if (seq_len<=1):
            self.temp_list[temp_index]=ele_pool[0]
            temp_seq_savg = self.temp_list[:]
            self.seq_list.append(temp_seq_savg)
        else:
            i = seq_len - 1
            while (i>=0):
                self.temp_list[temp_index] = ele_pool[i]
                temp_ele_pool = ele_pool[:]
                temp_ele_pool.pop(i)
                self.build_seq_list(seq_len-1,temp_ele_pool,temp_index-1)
                i -= 1
    
    def window_check (self):
        #self.debug.debug("* "+self.myInfo+" -- window_check",5) 
        
        temp_wait_list = []
        temp_wait_listB = []
        temp_last = -1
        temp_max = 1
        i = 1
        if (self.temp_check_len == 1):
            return [self.wait_job[0]['index']]
        
        while (i<=self.temp_check_len):
            temp_max = temp_max * i
            i += 1
            
        i = 0
        while (i<temp_max):
            j = 0
            temp_index = 0
            self.node_module.pre_reset(self.current_para['time'])
            while (j < self.temp_check_len):
                temp_node_req = {'proc':self.wait_job[self.seq_list[i][j]]['reqNodes']['proc']}
                temp_index =self.node_module.reserve(temp_node_req,\
                             self.wait_job[self.seq_list[i][j]]['index'], self.wait_job[self.seq_list[i][j]]['run'], index = temp_index)
                j += 1
            
            if (temp_last == -1 or temp_last>self.node_module.pre_get_last()['end']):
                temp_last = self.node_module.pre_get_last()['end']
                temp_wait_list = self.seq_list[i]
            i += 1
            
        i = 0
        while (i<self.temp_check_len):
            temp_wait_listB.append(self.wait_job[temp_wait_list[i]]['index'])
            i += 1
        
        return temp_wait_listB
             
    def adapt_reset(self):
        #self.debug.debug("* "+self.myInfo+" -- adapt_reset",5)
        self.adapt_data_name = []
        self.adapt_data_para = []
        self.check_data_name = []
        self.check_data_para = []
        self.avg_uti_interval = []
        self.avg_uti_index = []
        self.adapt_item = []
        self.bound_item = []
        self.adapt_info_name = "ad_win"
        if (self.para['ad_config'] and self.para['ad_mode'] != 0):
            self.adapt_read_config(self.para['ad_config'])
            
        i = 0
        while (i < len(self.avg_uti_interval)):
            item = float(self.avg_uti_interval[i])
            item_exist = 0
            j = 0
            while (j < len(self.info_module.avg_inter)):
                if item == self.info_module.avg_inter[j]:
                    item_exist = 1
                    break
                j += 1
            if (item_exist == 0):
                self.info_module.avg_inter.append(item)
            self.avg_uti_index.append(j)
            i += 1
                
        i = 0
        while (i < len(self.check_data_name)):
            if self.check_data_name[i] == 'avg_uti':
                self.check_data_para[i]=self.avg_uti_index[self.check_data_para[i]]
            i += 1
        self.info_module.reorder_avg_interval()
        
        '''
        self.debug.line(2,"**")
        self.debug.debug(self.adapt_data_name,2)
        self.debug.debug(self.adapt_data_para,2)
        self.debug.debug(self.check_data_name,2)
        self.debug.debug(self.check_data_para,2)
        self.debug.debug(self.avg_uti_interval,2)
        self.debug.debug(self.adapt_item,2)
        self.debug.debug(self.info_module.avg_uti_interval,2)
        self.debug.line(2,"**")
        '''
        
    def set_adapt_data (self):
        if self.para['ad_mode'] == 0:
            return
        adapt_data_num = 2
        end_index = len(self.info_module.sys_info) - 1
        self.info_module.sys_info[end_index][self.get_adapt_info_name()] = []
        i = 0
        while (i < adapt_data_num):
            self.info_module.sys_info[end_index][self.get_adapt_info_name()].append(0)
            i += 1
        # -1:down 0:equal 1:up
        # 0:no adapt 1:adapt
        if (end_index==0):
            self.info_module.sys_info[end_index][self.get_adapt_info_name()][0] = 0
            self.info_module.sys_info[end_index][self.get_adapt_info_name()][1] = 0
            return
        
        temp_uti_1 = self.info_module.sys_info[end_index]['avg_uti'][self.avg_uti_index[0]]
        temp_uti_2 = self.info_module.sys_info[end_index]['avg_uti'][self.avg_uti_index[1]]
        if (temp_uti_1<temp_uti_2):
            self.info_module.sys_info[end_index][self.get_adapt_info_name()][0] = -1
        elif (temp_uti_1==temp_uti_2):
            self.info_module.sys_info[end_index][self.get_adapt_info_name()][0] = self.info_module.sys_info[end_index-1][self.get_adapt_info_name()][0]
        else:
            self.info_module.sys_info[end_index][self.get_adapt_info_name()][0] = 1
            
        temp_uti_3 = self.info_module.sys_info[end_index-1][self.get_adapt_info_name()][0]
        temp_uti_4 = self.info_module.sys_info[end_index][self.get_adapt_info_name()][0]
        if (temp_uti_3 == temp_uti_4 or temp_uti_3 == 0):
            self.info_module.sys_info[end_index][self.get_adapt_info_name()][1] = 0
        else:
            self.info_module.sys_info[end_index][self.get_adapt_info_name()][1] = temp_uti_4
            
    def get_adapt_info_name(self):
        return self.adapt_info_name
        
    def adapt_read_config(self,fileName):
        #self.debug.debug("* "+self.myInfo+" -- adapt_read_config",5)
        self.adapt_data_name = []
        self.adapt_data_para = []
        self.check_data_name = []
        self.check_data_para = []
        self.avg_uti_interval = []
        self.avg_uti_index = []
        self.adapt_item = []
        self.bound_item = []
        
        regex_str = "([^=\\n]+)[=\\n]*"
        configFile = open(fileName,'r')
        temp_bound = []
                
        while (1):
            tempStr = configFile.readline()
            if not tempStr :    # break when no more line
                break
            temp_dataList=re.findall(regex_str,tempStr)
            #self.debug.debug(temp_dataList,2)
            if (temp_dataList[0] == 'adapt_data_name'):
                self.adapt_data_name = self.get_list(temp_dataList[1])
            if (temp_dataList[0] == 'adapt_data_para'):
                temp_list=self.get_list(temp_dataList[1])
                i = 0
                while i<len(temp_list):
                    temp_list[i] = int(temp_list[i])
                    i += 1
                self.adapt_data_para = temp_list
            elif (temp_dataList[0] == 'check_data_name'):
                self.check_data_name = self.get_list(temp_dataList[1])
            elif (temp_dataList[0] == 'check_data_para'):
                temp_list=self.get_list(temp_dataList[1])
                i = 0
                while i<len(temp_list):
                    temp_list[i] = int(temp_list[i])
                    i += 1
                self.check_data_para = temp_list
            elif (temp_dataList[0] == 'avg_uti'):
                temp_list=self.get_list(temp_dataList[1])
                i = 0
                while i<len(temp_list):
                    temp_list[i] = int(temp_list[i])
                    i += 1
                self.avg_uti_interval = temp_list
            elif (temp_dataList[0] == 'adapt_item'):
                temp_list=self.get_list(temp_dataList[1])
                i = 0
                while i<len(temp_list):
                    temp_list[i] = int(temp_list[i])
                    i += 1
                self.adapt_item.append(temp_list)
            elif (temp_dataList[0] == 'bound_item'):
                temp_list=self.get_list(temp_dataList[1])
                i = 0
                while i<len(temp_list):
                    temp_list[i] = int(temp_list[i])
                    i += 1
                temp_bound.append(temp_list)
                
        configFile.close()
        for temp_i in self.adapt_data_name:
            self.bound_item.append([0,0])
        #print self.adapt_data_name
        #print fileName
        for item in temp_bound:
            self.bound_item[item[0]] = [item[1],item[2]]
        
        return 1
    
    def window_adapt(self,para_in=[]):
        #self.debug.debug("* "+self.myInfo+" -- alg_adapt",5)
        self.ad_current_para = para_in
        if (self.para['ad_mode'] == 1):
            return self.adapt_1()
        return 0
        
    def adapt_1(self):
        action = 0
        max_check = len(self.check_data_name)
        end_index = len(self.info_module.sys_info) - 1
        action_b = 0
        for item in self.adapt_item:
            i = 0
            action = 1
            while (i < max_check and action == 1):
                if (self.check_data_para[i] == -1):
                    temp_para_1 = self.info_module.sys_info[end_index][self.check_data_name[i]]
                else:
                    temp_para_1 = self.info_module.sys_info[end_index][self.check_data_name[i]][self.check_data_para[i]]
                if (temp_para_1>=item[i*2+3] and temp_para_1<item[i*2+4]):
                    action = 1
                else:
                    action = 0
                i += 1
            '''
            self.debug.line(2,"**")
            self.debug.line(2,"**")
            self.debug.debug(item,2)
            self.debug.debug("3:"+str(item[0*2+3])+"   4:"+str(item[0*2+4])+"   t:"+str(temp_para_1),2)
            self.debug.debug("m:"+str(max_check)+"   i:"+str(i)+"   a:"+str(action),2)
            self.debug.line(2,"**")
            self.debug.line(2,"**")
            '''
            if (action != 0):
                action_b += 1
                if (item[1]==0):
                    if (self.adapt_data_para[item[0]] == -1):
                        self.para[self.adapt_data_name[item[0]]] = item[2]
                    else:
                        self.para[self.adapt_data_name[item[0]]][self.adapt_data_para[item[0]]] = item[2]  
                elif (item[1]==1):
                    if (self.adapt_data_para[item[0]] == -1):
                        self.para[self.adapt_data_name[item[0]]] = int(self.para[self.adapt_data_name[item[0]]]) + item[2]
                        if (self.para[self.adapt_data_name[item[0]]]<self.bound_item[item[0]][0]):
                            self.para[self.adapt_data_name[item[0]]]=self.bound_item[item[0]][0]
                        elif (self.para[self.adapt_data_name[item[0]]]>self.bound_item[item[0]][1]):
                            self.para[self.adapt_data_name[item[0]]]=self.bound_item[item[0]][1]
                    else:
                        self.para[self.adapt_data_name[item[0]]][self.adapt_data_para[item[0]]] = int(self.para[self.adapt_data_name[item[0]]][self.adapt_data_para[item[0]]]) + item[2]
                        if (self.para[self.adapt_data_name[item[0]]][self.adapt_data_para[item[0]]]<self.bound_item[item[0]][0]):
                            self.para[self.adapt_data_name[item[0]]][self.adapt_data_para[item[0]]]=self.bound_item[item[0]][0]
                        elif (self.para[self.adapt_data_name[item[0]]][self.adapt_data_para[item[0]]]>self.bound_item[item[0]][1]):
                            self.para[self.adapt_data_name[item[0]]][self.adapt_data_para[item[0]]]=self.bound_item[item[0]][1]
        return action_b
    
    def get_list (self,inputstring,regex=r'([^,]+)'):
        return re.findall(regex,inputstring)
    
    def get_adapt_list (self):
        result_list = []
        i = 0
        while(i<len(self.adapt_data_name)):
            if (self.adapt_data_para[i] == -1):
                result_list.append(self.para[self.adapt_data_name[i]])
            else:
                result_list.append(self.para[self.adapt_data_name[i]][self.adapt_data_para[i]]) 
            i += 1
        return result_list        