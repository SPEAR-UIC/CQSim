from datetime import datetime
import time
import re

__metaclass__ = type

class BurstBuffer_struc:
    def __init__(self, debug=None):
        self.myInfo = "BurstBuffer Structure"
        self.debug = debug
        self.job_list = []
        self.bb_vol_tot = []
        self.bb_avail = []
        self.bb_idle = []

        self.debug.line(4," ")
        self.debug.line(4,"#")
        self.debug.debug("# "+self.myInfo,1)
        self.debug.line(4,"#")

    def reset(self, debug=None):
        #self.debug.debug("* "+self.myInfo+" -- reset",5)
        self.debug = debug
        self.job_list = []
        self.bb_vol_tot = []
        self.bb_avail = []
        self.bb_idle = []
 

    def import_bb_config (self, config_file):
        #self.debug.debug("* "+self.myInfo+" -- import_node_config",5)
        regex_str = "([^=\\n]*)[=\\n]"
        bbFile = open(config_file,'r')
        config_data={}

        self.debug.line(4)
        while (1):
            tempStr = bbFile.readline()
            if not tempStr :    # break when no more line
                break
            temp_dataList=re.findall(regex_str,tempStr)
            config_data[temp_dataList[0]]=temp_dataList[1]
            if "BurstBuffer" in temp_dataList[0]:
                for res_str in temp_dataList[1].split(','):
                    vol = int(res_str)
                    self.bb_vol_tot.append(vol)
                    self.bb_avail.append(vol)
                    self.bb_idle.append(vol)
                break
            self.debug.debug(str(temp_dataList[0])+": "+str(temp_dataList[1]),4)
        self.debug.line(4)
        bbFile.close()

    def is_available(self, bb_vol):
        #self.debug.debug("* "+self.myInfo+" -- is_available",6)
        result = 0
        if self.bb_avail >= bb_vol:
            result = 1
        self.debug.debug("[Avail Check] "+str(result),6)
        return result


    def bb_allocate(self, bb_vol, job_index, start):
        if self.is_available(bb_vol) == 0:
            return 0
        self.bb_idle -= bb_vol
        self.bb_avail = self.bb_idle

        temp_job_info = {'job':job_index, 'bb': bb_vol}
        self.job_list.append(temp_job_info)
        self.debug.debug("  Allocate Job"+"["+str(job_index)+"]"+" Burst Buffer:"+str(bb_vol)+" Avail Burst Buffer:"+str(self.bb_avail)+" ",4)
        return 1

    def bb_release(self, job_index):
        j = 0
        temp_num = len(self.job_list)
        while (j<temp_num):
            if (job_index==self.job_list[j]['job']):
                self.bb_idle += self.job_list[j]['bb']
                self.bb_avail = self.bb_idle
                break
            j += 1
        self.job_list.pop(j)
        self.debug.debug("  Release Job"+"["+str(job_index)+"]"+" Avail Burst Buffer:"+str(self.bb_avail)+" ",4)
        return 1

    def get_bb_job_list(self):
        temp_job_index_list = []
        i = 0
        while(i<len(self.job_list)):
            temp_job_index_list.append(self.job_list[i]['job'])
            i += 1
        return temp_job_index_list

    def get_bb_tot(self):
        #self.debug.debug("* "+self.myInfo+" -- get_tot",6)
        return self.bb_vol_tot

    def get_bb_avail(self):
        #self.debug.debug("* "+self.myInfo+" -- get_avail",6)
        return self.bb_avail

    def get_bb_idle(self):
        #self.debug.debug("* "+self.myInfo+" -- get_idle",6)
        return self.bb_idle
   