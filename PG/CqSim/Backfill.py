
__metaclass__ = type
import random
import numpy as np

class Backfill:
    def __init__(self, mode = 0, ad_mode = 0, node_module = None, debug = None, para_list = None):
        self.myInfo = "Backfill"
        self.mode = mode
        self.ad_mode = ad_mode
        self.node_module = node_module
        self.debug = debug
        self.para_list = para_list
        self.current_para = []
        self.wait_job = []

        self.debug.line(4," ")
        self.debug.line(4,"#")
        self.debug.debug("# "+self.myInfo,1)
        self.debug.line(4,"#")
        
    def reset (self, mode = None, ad_mode = None, node_module = None, debug = None, para_list = None):
        #self.debug.debug("* "+self.myInfo+" -- reset",5)
        if mode:
            self.mode = mode
        if ad_mode :
            self.ad_mode = ad_mode 
        if node_module:
            self.node_module = node_module
        if debug:
            self.debug = debug
        if para_list:
            self.para_list = para_list
        self.current_para = []
        self.wait_job = []
    
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
        if (self.mode == 1):
            # EASY backfill
            result = self.backfill_EASY()
        elif (self.mode == 2):
            # Conservative backfill
            result = self.backfill_cons() 
        elif (self.mode == 3):
            result = self.backfill_RL() 
        else:
            return None
        return result

    def backfill_RL(self):
        max_idxs = []
        backfill_list=[]
        selected_fv_list = []
        self.node_module.pre_reset(self.current_para['time'])
        self.node_module.reserve(self.wait_job[0]['proc'], self.wait_job[0]['index'], self.wait_job[0]['run'])

        while True:
            backfill_candidates = []
            backfill_candidates_pos = []
            i = 1
            job_num = len(self.wait_job)
            while (i < job_num):
                backfill_test = 0
                backfill_test = self.node_module.pre_avail(self.wait_job[i]['proc'],\
                        self.current_para['time'], self.current_para['time']+self.wait_job[i]['run'])
                if (backfill_test == 1):
                    backfill_candidates.append(self.wait_job[i])
                    backfill_candidates_pos.append(i)
                    #backfill_list.append(self.wait_job[i]['index'])
                    #self.node_module.reserve(self.wait_job[i]['proc'], self.wait_job[i]['index'], self.wait_job[i]['run'])
                i += 1
            if not backfill_candidates:
                break
            else:
                self.debug.debug('backfill_candidates ....'+str(backfill_candidates),4)
                temp_nodeStruc = self.node_module.get_nodeStruc()
                #max_idx, selected_fv = self.current_para['alg_module'].compute_score(backfill_candidates, temp_nodeStruc, self.current_para['time'], epsilon = self.current_para['epsilon'])
                probabilities, selected_fv = self.current_para['alg_module'].compute_score_probabilities(backfill_candidates, temp_nodeStruc, self.current_para['time'], epsilon = self.current_para['epsilon'])
                if len(probabilities)>len(backfill_candidates):
                    probabilities = probabilities[:len(backfill_candidates)]
                    probabilities = [float(i)/sum(probabilities) for i in probabilities]
                #print("probabilities_norm",probabilities)
                if sum(probabilities)>0:
                    max_idx = np.random.choice(len(probabilities), p=probabilities)
                else:
                    #max_idx = random.randint(0, len(probabilities)-1)
                    max_idx = 0

                max_idxs.append(max_idx)
                backfill_list.append(backfill_candidates[max_idx]['index'])
                self.debug.debug('backfill_list_progress ....'+str(backfill_list)+" max_idx "+str(max_idx),4)
                selected_fv_list.append(selected_fv)

                self.node_module.reserve(backfill_candidates[max_idx]['proc'], backfill_candidates[max_idx]['index'], backfill_candidates[max_idx]['run'])

                self.wait_job = self.wait_job[:backfill_candidates_pos[max_idx]]+self.wait_job[backfill_candidates_pos[max_idx]+1:]

                '''
                #print('max_idx',max_idx, len(backfill_candidates))
                max_idxs.append(max_idx)
                if max_idx<0 or max_idx>=len(backfill_candidates):
                    #max_idx = 0
                    if -1 not in backfill_list:
                        backfill_list.append(-1)
                    else:
                        max_idx = random.randint(0, len(backfill_candidates)-1)
                        backfill_list.append(backfill_candidates[0]['index'])
                        self.node_module.reserve(backfill_candidates[max_idx]['proc'], backfill_candidates[max_idx]['index'], backfill_candidates[max_idx]['run'])

                        self.wait_job = self.wait_job[:backfill_candidates_pos[max_idx]]+self.wait_job[backfill_candidates_pos[max_idx]+1:]
                        #break
                    self.debug.debug('backfill_list_progress ....'+str(backfill_list)+" max_idx "+str(max_idx),4)
                    selected_fv_list.append(selected_fv)
                    #print('backfill_list',backfill_list)
                    #break #?
                else:
                    backfill_list.append(backfill_candidates[max_idx]['index'])
                    self.debug.debug('backfill_list_progress ....'+str(backfill_list)+" max_idx "+str(max_idx),4)
                    selected_fv_list.append(selected_fv)

                    self.node_module.reserve(backfill_candidates[max_idx]['proc'], backfill_candidates[max_idx]['index'], backfill_candidates[max_idx]['run'])

                    self.wait_job = self.wait_job[:backfill_candidates_pos[max_idx]]+self.wait_job[backfill_candidates_pos[max_idx]+1:]
                '''

        return backfill_list, selected_fv_list, max_idxs


    
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
            
        self.node_module.reserve(self.wait_job[0]['proc'], self.wait_job[0]['index'], self.wait_job[0]['run'])
        i = 1
        job_num = len(self.wait_job)
        while (i < job_num):
            backfill_test = 0
            backfill_test = self.node_module.pre_avail(self.wait_job[i]['proc'],\
                    self.current_para['time'], self.current_para['time']+self.wait_job[i]['run'])
            if (backfill_test == 1):
                backfill_list.append(self.wait_job[i]['index'])
                self.node_module.reserve(self.wait_job[i]['proc'], self.wait_job[i]['index'], self.wait_job[i]['run'])
            i += 1
        return backfill_list
        
    def backfill_cons(self):
        #self.debug.debug("* "+self.myInfo+" -- backfill_cons",5)
        backfill_list=[]
        self.node_module.pre_reset(self.current_para['time'])
        self.node_module.reserve(self.wait_job[0]['proc'], self.wait_job[0]['index'], self.wait_job[0]['run'])
        i = 1
        job_num = len(self.wait_job)
        while (i < job_num):
            backfill_test = 0
            backfill_test = self.node_module.pre_avail(self.wait_job[i]['proc'],\
                    self.current_para['time'], self.current_para['time']+self.wait_job[i]['run'])
            if (backfill_test == 1):
                backfill_list.append(self.wait_job[i]['index'])
            self.node_module.reserve(self.wait_job[i]['proc'], self.wait_job[i]['index'], self.wait_job[i]['run'])
            i += 1  
        return backfill_list
    