
__metaclass__ = type
class Start_window:
    def __init__(self, mode = 0, ad_mode = 0, node_module = None, debug = None, para_list = [6,0,0], para_list_ad = None):
        self.myInfo = "Start Window"
        self.mode = mode
        self.ad_mode = ad_mode
        self.node_module = node_module
        self.debug = debug
        self.para_list = para_list
        self.para_list_ad = para_list_ad
        #print self.para_list
        if (len(self.para_list)>=1 and int(self.para_list[0]) > 0):
            self.win_size = int(self.para_list[0])
        else:
            self.win_size = 1
        if (len(self.para_list)>=2 and int(self.para_list[1]) > 0):
            self.check_size_in = int(self.para_list[1])
        else:
            self.check_size_in = self.win_size
        if (len(self.para_list)>=3 and int(self.para_list[2]) > 0):
            self.max_start_size = int(self.para_list[2])
        else:
            self.max_start_size = self.win_size
            
        self.temp_check_len = self.check_size_in
        
        self.current_para = []
        self.seq_list = []

        self.debug.line(4," ")
        self.debug.line(4,"#")
        self.debug.debug("# "+self.myInfo,1)
        self.debug.line(4,"#")
        
        self.reset_list()
        
    def reset (self, mode = None,  ad_mode = None, node_module = None, debug = None, para_list = None, para_list_ad = None):
        #self.debug.debug("* "+self.myInfo+" -- reset",5) 
        if mode:
            self.mode = mode
        if ad_mode:
            self.ad_mode =ad_mode
        if node_module:
            self.node_module = node_module
        if debug:
            self.debug = debug
        if para_list:
            self.para_list = para_list
            if (self.para_list[0] and self.para_list[0] > 0):
                self.win_size = self.para_list[0]
            else:
                self.win_size = 1
            if (self.para_list[1] and self.para_list[1] > 0):
                self.check_size_in = self.para_list[1]
            else:
                self.check_size_in = self.win_size
            if (self.para_list[2] and self.para_list[2] > 0):
                self.max_start_size = self.para_list[2]
            else:
                self.max_start_size = self.win_size
                
        if para_list_ad:
            self.para_list_ad = para_list_ad
            
        self.current_para = []
        self.seq_list = []
        self.reset_list()
    
    def start_window (self, wait_job, para_in = None):
        #self.debug.debug("* "+self.myInfo+" -- start_window",5) 
        self.current_para = para_in
        temp_len = len(wait_job)
        self.wait_job = []
        i = 0
        while (i < self.win_size and i < temp_len):
            self.wait_job.append(wait_job[i])
            i += 1
        if i>self.check_size_in:
            i = self.check_size_in
        self.temp_check_len = i
        result = self.main()
        return result
    
    def main (self):
        #self.debug.debug("* "+self.myInfo+" -- main",5) 
        result = []
        if self.mode == 1:
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
    
    def window_adapt (self, para_in = None):
        #self.debug.debug("* "+self.myInfo+" -- window_adapt",5) 
        return 0
    
    def window_size (self):
        #self.debug.debug("* "+self.myInfo+" -- window_size",6) 
        return self.win_size
    
    def check_size (self):
        #self.debug.debug("* "+self.myInfo+" -- check_size",6) 
        return self.check_size_in
    
    def start_num (self):
        #self.debug.debug("* "+self.myInfo+" -- start_num",6) 
        return self.max_start_size
    
    def reset_list (self):
        #self.debug.debug("* "+self.myInfo+" -- reset_list",5) 
        self.seq_list = []
        self.temp_list=[]
        self.wait_job = []
        temp_seq=[]
        i = 0
        ele = []
        while (i<self.check_size_in):
            ele.append(i)
            self.temp_list.append(-1)
            i += 1
        self.build_seq_list(self.check_size_in, ele, self.check_size_in-1)

    def build_seq_list(self, seq_len, ele_pool, temp_index):
        #self.debug.debug("* "+self.myInfo+" -- build_seq_list",6) 
        if (seq_len<=1):
            self.temp_list[temp_index]=ele_pool[0]
            temp_seq_save = self.temp_list[:]
            self.seq_list.append(temp_seq_save)
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
                temp_index =self.node_module.reserve(self.wait_job[self.seq_list[i][j]]['proc'],\
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
        