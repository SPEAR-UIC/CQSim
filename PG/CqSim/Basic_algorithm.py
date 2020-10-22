import numpy as np

__metaclass__ = type

class Basic_algorithm:
    def __init__ (self, ad_mode = 0, element = None, debug = None, para_list = None, ad_para_list=None, learning_model = None):
        self.myInfo = "Basic Algorithm"
        self.ad_mode = ad_mode
        self.element = element
        self.debug = debug
        self.paralist = para_list
        self.ad_paralist = ad_para_list
        self.model = learning_model
        
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

    def preprocessing_queued_jobs(self, wait_job, currentTime):
        job_info_list = []
        waitNum = len(wait_job)
        i=0
        while (i<waitNum):
            s = float(wait_job[i]['submit'])
            t = float(wait_job[i]['reqTime'])
            n = float(wait_job[i]['reqProc'])
            w = int(currentTime - s)
            # award 1: high priority; 0: low priority
            a = int(wait_job[i]['award'])
            #info = [n, t, 1, w]
            info = [[n, t], [a, w]]
            job_info_list.append(info)
            i += 1
        return job_info_list

    def preprocessing_system_status(self, node_struc, currentTime):
        node_info_list = []
        for node in node_struc:
            info = []
            # avabile 1, not available 0
            if node['state'] <0:
                info.append(1)
                info.append(0)
            else:
                info.append(0)
                info.append(node['end']-currentTime)
            node_info_list.append(info)
        return node_info_list

    def make_feature_vector(self, jobs, system_status):
        #print('self.model.job_cols',self.model.job_cols)
        job_cols = self.model.job_cols
        window_size = self.model.get_window_size()
        input_dim = [len(system_status)+window_size*job_cols, len(system_status[0])]
        #print('input_dim',input_dim)
        # build a feature vector from the current board
        #fv_size = 100+1 #?
        # create empty feature vector
        fv = np.zeros((1, input_dim[0], input_dim[1])) # ?
        # set X locations
        #fv[:len(jobs), 0:job_cols, :] = jobs #?
        i = 0
        for idx,job in enumerate(jobs):
            fv[0, idx*job_cols:(idx+1)*job_cols, :] = job
            i += 1
            if i == window_size:
                break
        fv[0, job_cols*window_size:, :] = system_status
        #print('fv.shape',fv.shape)
        #print('fv',fv)
        return fv

    def make_random_choice(self,wait_job):
        job_idx = np.random.choice(range(len(wait_job)))
        return job_idx

    def compute_score_probabilities(self, wait_job, node_struc, currentTime, para_list = None, epsilon = 0.25, backfill = False):
        #self.debug.debug("* "+self.myInfo+" -- get_score",5)
        #self.scoreList = []
        waitNum = len(wait_job)
        if (waitNum<=0):
            #return []
            return -1
        else:
            '''
            i=0
            while (i<waitNum):
                s = float(wait_job[i]['submit'])
                t = float(wait_job[i]['reqTime'])
                n = float(wait_job[i]['reqProc'])
                w = int(currentTime - s)
                self.scoreList.append(float(eval(self.algStr)))
                i += 1
            '''
            #pass
            feature_vectors = None
            wait_job_input = self.preprocessing_queued_jobs(wait_job, currentTime)
            system_status_input = self.preprocessing_system_status(node_struc, currentTime)
            feature_vectors = self.make_feature_vector(wait_job_input,system_status_input)
            probabilities = []
            if not backfill:

                probabilities = self.model.get_probabilities(feature_vectors)
                window_size = self.model.window_size
                '''
                if job_idx >= window_size:
                    job_idx = -1
                '''

    
        return probabilities, feature_vectors
        #self.debug.debug("  Score:"+str(self.scoreList),4)
        #return values


    def compute_score(self, wait_job, node_struc, currentTime, para_list = None, epsilon = 0.25, backfill = False):
        #self.debug.debug("* "+self.myInfo+" -- get_score",5)
        #self.scoreList = []
        waitNum = len(wait_job)
        if (waitNum<=0):
            #return []
            return -1
        else:
            '''
            i=0
            while (i<waitNum):
                s = float(wait_job[i]['submit'])
                t = float(wait_job[i]['reqTime'])
                n = float(wait_job[i]['reqProc'])
                w = int(currentTime - s)
                self.scoreList.append(float(eval(self.algStr)))
                i += 1
            '''
            #pass
            feature_vectors = None
            wait_job_input = self.preprocessing_queued_jobs(wait_job, currentTime)
            system_status_input = self.preprocessing_system_status(node_struc, currentTime)
            feature_vectors = self.make_feature_vector(wait_job_input,system_status_input)
            if not backfill:

                job_idx = self.model.choose_action(feature_vectors)
                window_size = self.model.window_size
                '''
                if job_idx >= window_size:
                    job_idx = -1
                '''

            else:
                job_idx = 0

    
        return job_idx, feature_vectors
        #self.debug.debug("  Score:"+str(self.scoreList),4)
        #return values
            
    def log_analysis(self):
        #self.debug.debug("* "+self.myInfo+" -- log_analysis",5)
        return 1
            
    def alg_adapt(self, para_in):
        #self.debug.debug("* "+self.myInfo+" -- alg_adapt",5)
        return 1
            
            