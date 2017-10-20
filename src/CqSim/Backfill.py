import cqsim_path
import re

__metaclass__ = type

class Backfill:
    def __init__(self, mode = 0, ad_mode = 0, node_module = None, info_module = None, debug = None, para_list = None, ad_para_list = None):
        self.myInfo = "Backfill"
        self.para={}
        self.para['mode'] = mode
        self.para['ad_mode'] = ad_mode
        self.para['size'] = 0
        if para_list:
            self.para['size'] = para_list[0]
        if ad_para_list:
            self.para['ad_config'] = cqsim_path.path_config+ad_para_list[0]
        else:
            self.para['ad_config'] = None
        self.node_module = node_module
        self.info_module = info_module
        self.debug = debug
        self.para_list_in = para_list
        self.ad_para_list_in = ad_para_list
        self.ad_current_para = []
        self.current_para = []
        self.wait_job = []
        self.show_module_info()
        
        self.adapt_reset()
        
    def reset (self, mode = None, ad_mode = None, node_module = None, info_module = None, debug = None, para_list = None, ad_para_list = None):
        #self.debug.debug("* "+self.myInfo+" -- reset",5)
        if mode:
            self.para['mode'] = mode
        if ad_mode :
            self.para['ad_mode'] = ad_mode 
        if ad_para_list:
            self.ad_para_list_in = ad_para_list 
            self.para['ad_config'] = ad_para_list[0]
        if node_module:
            self.node_module = node_module
        if info_module:
            self.info_module = info_module
        if debug:
            self.debug = debug
        if para_list:
            self.para_list_in = para_list
            self.para['size'] = para_list[0]
        self.current_para = []
        self.wait_job = []
        self.current_para = []
        self.adapt_reset()
    
    def show_module_info (self):
        #self.debug.line(1," ")
        self.debug.debug("-- "+self.myInfo,1)  
    
    def backfill (self, wait_job, para_in = None):
        #self.debug.debug("* "+self.myInfo+" -- backfill",5)
        if (len(wait_job) <= 1):
            return []
        self.current_para = para_in
        self.wait_job = wait_job
        job_list = self.main()
        return job_list
    
    def main (self):
        #self.debug.debug("* "+self.myInfo+" -- main",5)
        result = []
        if (self.para['mode'] == 1):
            # EASY backfill
            result = self.backfill_EASY()
        elif (self.para['mode'] == 2):
            # Conservative backfill
            result = self.backfill_cons() 
        else:
            return None
        return result
    
    def backfill_EASY(self):
        #self.debug.debug("* "+self.myInfo+" -- backfill_EASY",5)
        backfill_list=[]
        self.node_module.pre_reset(self.current_para['time'])
        '''
        self.debug.line(4,'.')
        for job in self.wait_job:
            self.debug.debug(job,4)
        self.debug.line(4,'.')
        '''
            
        temp_node_req = self.wait_job[0]['reqNodes']
        self.node_module.reserve(temp_node_req, self.wait_job[0]['index'], self.wait_job[0]['run'])
        i = 1
        job_num = len(self.wait_job)
        while (i < job_num):
            backfill_test = 0
            temp_node_req2 = self.wait_job[i]['reqNodes']
            backfill_test = self.node_module.pre_avail(temp_node_req2,\
                    self.current_para['time'], self.current_para['time']+self.wait_job[i]['run'])
            if (backfill_test == 1):
                backfill_list.append(self.wait_job[i]['index'])
                self.node_module.reserve(temp_node_req2, self.wait_job[i]['index'], self.wait_job[i]['run'])
            i += 1
        return backfill_list
        
    def backfill_cons(self):
        #self.debug.debug("* "+self.myInfo+" -- backfill_cons",5)
        backfill_list=[]
        self.node_module.pre_reset(self.current_para['time'])
        temp_node_req = self.wait_job[0]['reqNodes']
        self.node_module.reserve(temp_node_req, self.wait_job[0]['index'], self.wait_job[0]['run'])
        i = 1
        job_num = len(self.wait_job)
        while (i < job_num):
            backfill_test = 0
            temp_node_req2 = self.wait_job[i]['reqNodes']
            backfill_test = self.node_module.pre_avail(temp_node_req2,\
                    self.current_para['time'], self.current_para['time']+self.wait_job[i]['run'])
            if (backfill_test == 1):
                backfill_list.append(self.wait_job[i]['index'])
            self.node_module.reserve(temp_node_req2, self.wait_job[i]['index'], self.wait_job[i]['run'])
            i += 1  
        return backfill_list
    
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
        self.adapt_info_name = "ad_bf"
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
        self.debug.debug(self.bound_item,2)
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
        for item in temp_bound:
            self.bound_item[item[0]] = [item[1],item[2]]
        
        return 1
    
    def backfill_adapt (self,para_in=[]):
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
                        self.para[self.adapt_data_name[item[0]]] += item[2]
                        if (self.para[self.adapt_data_name[item[0]]]<self.bound_item[item[0]][0]):
                            self.para[self.adapt_data_name[item[0]]]=self.bound_item[item[0]][0]
                        elif (self.para[self.adapt_data_name[item[0]]]>self.bound_item[item[0]][1]):
                            self.para[self.adapt_data_name[item[0]]]=self.bound_item[item[0]][1]
                    else:
                        self.para[self.adapt_data_name[item[0]]][self.adapt_data_para[item[0]]] += item[2]
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
    