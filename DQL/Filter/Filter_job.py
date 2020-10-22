from datetime import datetime
import time

__metaclass__ = type

class Filter_job:
    def __init__(self, trace, save=None, config=None, sdate=None, start=-1, density=1.0, anchor=0, rnum=0, debug=None):
        self.myInfo = "Filter Job"
        self.start = start
        self.sdate = sdate
        self.density = float(density)
        self.anchor = int(anchor)
        self.rnum = int(rnum)
        self.trace = str(trace)
        self.save = str(save)
        self.config = str(config)
        self.debug = debug
        self.jobNum = -1
        self.jobList=[]
        
        self.debug.line(4," ")
        self.debug.line(4,"#")
        self.debug.debug("# "+self.myInfo,1)
        self.debug.line(4,"#")
        
        self.reset_config_data()
    
    def reset(self, trace=None, save=None, config=None, sdate=None, start=None, density=None, anchor=None, rnum=None, debug=None):
        self.debug.debug("* "+self.myInfo+" -- reset",5) 
        if start:
            self.start = start
        if sdate:
            self.sdate = sdate
        if density:
            self.density = float(density)
        if anchor:
            self.anchor = int(anchor)
        if rnum:
            self.rnum = int(rnum)
        if trace:
            self.trace = str(trace)
        if save:
            self.save = str(save)
        if config:
            self.config = str(config)
        if debug:
            self.debug = debug
        self.jobNum = -1
        self.jobList=[]
        
        self.reset_config_data()
    
    def reset_config_data(self):
        self.debug.debug("* "+self.myInfo+" -- reset_config_data",5) 
        self.config_start=';'
        self.config_sep='\\n'
        self.config_equal=': '
        self.config_data=[]
        #self.config_data.append({'name_config':'date','name':'StartTime','value':''})
        
    def read_job_trace(self):
        self.debug.debug("* "+self.myInfo+" -- read_job_trace",5) 
        return
    
    def input_check(self,jobInfo):
        self.debug.debug("* "+self.myInfo+" -- input_check",5) 
        return

    def get_job_num(self):
        self.debug.debug("* "+self.myInfo+" -- get_job_num",6) 
        return self.jobNum

    def get_job_data(self):
        self.debug.debug("* "+self.myInfo+" -- get_job_data",5) 
        return self.jobList
    
    def output_job_data(self):
        self.debug.debug("* "+self.myInfo+" -- output_job_data",5) 
        if not self.save:
            print("Save file not set!")
            return
        return
    
    def output_job_config(self):
        self.debug.debug("* "+self.myInfo+" -- output_job_config",5) 
        if not self.config:
            print("Config file not set!")
            return
        return
    
