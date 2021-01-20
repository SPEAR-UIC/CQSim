
__metaclass__ = type

class Basic_algorithm:
    def __init__ (self, ad_mode = 0, element = None, debug = None, para_list = None, ad_para_list=None):
        self.myInfo = "Basic Algorithm"
        self.ad_mode = ad_mode
        self.element = element
        self.debug = debug
        self.paralist = para_list
        self.ad_paralist = ad_para_list
        
        self.debug.line(4," ")
        self.debug.line(4,"#")
        self.debug.debug("# "+self.myInfo,1)
        self.debug.line(4,"#")
        
        self.algStr=""
        self.scoreList=[]
        i = 0
        temp_num = len(self.element[0])
        while (i < temp_num):
            self.algStr += self.element[0][i]
            i += 1
    
    def reset (self, ad_mode = None, element = None, debug = None, para_list = None, ad_para_list=None):
        #self.debug.debug("* "+self.myInfo+" -- reset",5)
        if ad_mode :
            self.ad_mode = ad_mode 
        if element:
            self.element = element
        if debug:
            self.debug = debug
        if paralist:
            self.paralist = paralist
            
        self.algStr=""
        self.scoreList=[]
        i = 0
        temp_num = len(self.element[0])
        while (i < temp_num):
            self.algStr += self.element[0][i]
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
            
    def log_analysis(self):
        #self.debug.debug("* "+self.myInfo+" -- log_analysis",5)
        return 1
            
    def alg_adapt(self, para_in):
        #self.debug.debug("* "+self.myInfo+" -- alg_adapt",5)
        return 1
            
            