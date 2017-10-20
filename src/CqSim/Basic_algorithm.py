import cqsim_path
import re
__metaclass__ = type

class Basic_algorithm:
    def __init__ (self, ad_mode = 0, element = None, info_module = None, debug = None, ad_para_list=None):
        self.myInfo = "Basic Algorithm"
        self.para={}
        self.para['ad_mode'] = ad_mode
        
        i = 0
        self.para['element'] = []
        self.para['sign'] = []
        while (i < len (element[0])):
            self.para['element'].append(element[0][i])
            self.para['sign'].append(element[1][i])
            i += 1
            
        self.info_module = info_module
        self.debug = debug
        self.ad_para_list = ad_para_list
        
        if ad_para_list:
            self.para['ad_config'] = cqsim_path.path_config+ad_para_list[0]
        else:
            self.para['ad_config'] = None
        self.show_module_info()
        
        self.algStr=""
        self.scoreList=[]
        self.build_alg_str()
        self.adapt_reset()
    
    def reset (self, ad_mode = None, element = None, info_module = None, debug = None, ad_para_list=None):
        #self.debug.debug("* "+self.myInfo+" -- reset",5)
        if ad_mode :
            self.para['ad_mode'] = ad_mode 
        if element:
            i = 0
            self.para['element'] = []
            self.para['sign'] = []
            while (i < len (element[0])):
                self.para['element'].append(element[0][i])
                self.para['sign'].append(element[1][i])
                i += 1
        if info_module:
            self.info_module = info_module
        if debug:
            self.debug = debug
        if ad_para_list:
            self.ad_para_list = ad_para_list
            self.para['ad_config'] = cqsim_path.path_config+ad_para_list[0]
            
        self.algStr=""
        self.scoreList=[]
        self.build_alg_str()
        self.adapt_reset()
    
    def show_module_info (self):
        #self.debug.line(1," ")
        self.debug.debug("-- "+self.myInfo,1)    
            
    def build_alg_str(self):
        self.algStr = ""
        i = 0
        temp_num = len(self.para['element'])
        while (i < temp_num):
            self.algStr += str(self.para['element'][i])
            i += 1
            
    def get_score(self, wait_job, currentTime, para_list = None):
        #self.debug.debug("* "+self.myInfo+" -- get_score",5)
        self.scoreList = []
        waitNum = len(wait_job)
        if (waitNum<=0):
            return []
        else:
            i=0
            z=currentTime - wait_job[0]['submit']
            l=wait_job[0]['reqTime']
            while (i<waitNum):
                temp_w = currentTime - wait_job[i]['submit']
                if (temp_w>z):
                    z=temp_w
                if (wait_job[i]['reqTime']<l):
                    l=wait_job[i]['reqTime']
                i+=1
            i=0
            if (z == 0):
                z = 1
            while (i<waitNum):
                s = float(wait_job[i]['submit'])
                t = float(wait_job[i]['reqTime'])
                n = float(wait_job[i]['reqProc'])
                w = int(currentTime - s)
                self.scoreList.append(float(eval(self.algStr)))
                i += 1
        #self.debug.debug("  Score:"+str(self.scoreList),4)
        return self.scoreList
                        
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
        self.adapt_info_name = "ad_alg"
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
        self.debug.debug(self.info_module.avg_inter,2)
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
        #print self.adapt_data_name
        #print fileName
        for item in temp_bound:
            self.bound_item[item[0]] = [item[1],item[2]]
        
        return 1
    
    def alg_adapt(self,para_in=[]):
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
                        self.para[self.adapt_data_name[item[0]]] = float(self.para[self.adapt_data_name[item[0]]]) + item[2]
                        if (self.para[self.adapt_data_name[item[0]]]<self.bound_item[item[0]][0]):
                            self.para[self.adapt_data_name[item[0]]]=self.bound_item[item[0]][0]
                        elif (self.para[self.adapt_data_name[item[0]]]>self.bound_item[item[0]][1]):
                            self.para[self.adapt_data_name[item[0]]]=self.bound_item[item[0]][1]
                    else:
                        self.para[self.adapt_data_name[item[0]]][self.adapt_data_para[item[0]]] = float(self.para[self.adapt_data_name[item[0]]][self.adapt_data_para[item[0]]]) + item[2]
                        if (self.para[self.adapt_data_name[item[0]]][self.adapt_data_para[item[0]]]<self.bound_item[item[0]][0]):
                            self.para[self.adapt_data_name[item[0]]][self.adapt_data_para[item[0]]]=self.bound_item[item[0]][0]
                        elif (self.para[self.adapt_data_name[item[0]]][self.adapt_data_para[item[0]]]>self.bound_item[item[0]][1]):
                            self.para[self.adapt_data_name[item[0]]][self.adapt_data_para[item[0]]]=self.bound_item[item[0]][1]
            
        if (action_b > 0):
            self.build_alg_str()   
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