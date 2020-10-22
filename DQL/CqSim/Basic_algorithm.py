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

    def make_feature_vector(self, job, system_status):
        #print('self.model.job_cols',self.model.job_cols)
        job_cols = self.model.job_cols
        input_dim = [len(system_status)+job_cols, len(system_status[0])]
        #print('input_dim',input_dim)
        # build a feature vector from the current board
        #fv_size = 100+1 #?
        # create empty feature vector
        fv = np.zeros((1, input_dim[0], input_dim[1])) # ?
        # set X locations
        fv[0, 0:job_cols, :] = job
        fv[0, job_cols:, :] = system_status
        #print('fv.shape',fv.shape)
        return fv

    def make_random_choice(self,wait_job):
        job_idx = np.random.choice(range(len(wait_job)))
        return job_idx


    def compute_score(self, wait_job, node_struc, currentTime, para_list = None, epsilon = 0.25):
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
            wait_job_input = self.preprocessing_queued_jobs(wait_job, currentTime)
            system_status_input = self.preprocessing_system_status(node_struc, currentTime)
            if np.random.random() < epsilon:
                #print('epsilon',epsilon)
                job_idx = self.make_random_choice(wait_job)
              # make the best move based on the current model
            else:
                #print('wait_job_input', wait_job_input)
                #print('system_status_input', system_status_input)
                #input_dim = []
                feature_vectors = np.vstack([self.make_feature_vector(job,system_status_input) for job in wait_job_input])
                values = self.model(feature_vectors)
                values = values.numpy()
                
                job_idx = np.argmax(values)
                #print('values',values, 'max_idx', job_idx)

            fv = None
            if job_idx>=0:
                fv = self.make_feature_vector(wait_job_input[job_idx],system_status_input)
    
        return job_idx, fv
        #self.debug.debug("  Score:"+str(self.scoreList),4)
        #return values
            
    def log_analysis(self):
        #self.debug.debug("* "+self.myInfo+" -- log_analysis",5)
        return 1
            
    def alg_adapt(self, para_in):
        #self.debug.debug("* "+self.myInfo+" -- alg_adapt",5)
        return 1
            
            