from datetime import datetime
import time
__metaclass__ = type

class Info_collect:
    def __init__(self, alg_module = None, debug = None):
        self.myInfo = "Info Collect"
        self.alg_module = alg_module
        self.debug = debug
        #self.sys_info = []
        
        self.debug.line(4," ")
        self.debug.line(4,"#")
        self.debug.debug("# "+self.myInfo,1)
        self.debug.line(4,"#")
        
        
    def reset(self, alg_module = None, debug = None):
        self.debug.debug("* "+self.myInfo+" -- reset",5)
        if alg_module:
            self.alg_module = alg_module
        if debug:
            self.debug = debug
        #self.sys_info = []
        
    def info_collect(self, time, event, uti, waitNum = -1, waitSize = -1, waitCore = -1, inter = -1.0, extend = None):
        self.debug.debug("* "+self.myInfo+" -- info_collect",5)
        event_date = time
        temp_info = {'date': event_date, 'time': time, 'event': event, 'uti': uti, 'waitNum': waitNum, \
                     'waitSize': waitSize, 'waitCore':waitCore, 'inter': inter, 'extend': extend}
        self.debug.debug("   "+str(temp_info),4) 
        #self.sys_info.append(temp_info)
        return temp_info
    
    '''
    def info_analysis(self):
        self.debug.debug("* "+self.myInfo+" -- info_analysis",5)
        return 1
    
    
    def get_info(self, index):
        self.debug.debug("* "+self.myInfo+" -- get_info",6)
        if index>=len(self.sys_info):
            return None
        return self.sys_info[index]
    
    def get_len(self):
        self.debug.debug("* "+self.myInfo+" -- get_len",6)
        return len(self.sys_info)
    '''