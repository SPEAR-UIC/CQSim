import random
import numpy as np
import logging,copy,os,sys
from collections import Counter
import tensorflow as tf
import keras.backend as K
#import matplotlib.pyplot as plt
#import IPython.display as ipydis
# turn off all the deprecation warnings
'''
tf.logging.set_verbosity(logging.ERROR)
# turn on eager execution
tf.enable_eager_execution()
tfe = tf.contrib.eager
print('Tensorflow Version: %s',tf.__version__)

'''

class ValueModel():
    def __init__(self, mode = 0, debug = None, input_dim_str = '2', job_cols=1, window_size = 5, hidden_dim_str = '1000,250', node_module=None, GAMMA=0.99, ALPHA = 0.01, fname='reinforce.h5'): 
        self.myInfo = "ValueModel"
        self.debug = debug

        self.job_cols = job_cols
        self.window_size = window_size

        self.hidden_dim = []

        if node_module:
            self.input_dim = [node_module.get_tot()+self.window_size*self.job_cols]
        else:
            self.input_dim = [100+self.window_size*self.job_cols]

        for e in input_dim_str.split(','):
            self.input_dim.append(int(e))

        for e in hidden_dim_str.split(','):
            self.hidden_dim.append(int(e))

        print('input_dim',self.input_dim)
        print('hidden_dim',self.hidden_dim)

        self.gamma = float(GAMMA)
        self.lr = ALPHA
        self.G = 0
        #self.input_dim = input_dim
        #self.hidden_dim = hidden_dim
        self.n_actions = self.window_size

        self.state_memory = []
        self.action_memory = []
        self.reward_memory = []
        self.policy, self.predict = self.build_policy_network()
        self.action_space = [i for i in range(self.n_actions)]

        self.model_file = fname

        print('start value model ____________')

    def get_window_size(self):
        return self.window_size

    def build_policy_network(self):
        input = tf.keras.layers.Input(shape=(self.input_dim[0],self.input_dim[1]))
        advantages = tf.keras.layers.Input(shape=[1])
        input_reshape = tf.reshape(input,[-1,self.input_dim[1],1])
        conv1d = tf.keras.layers.Conv1D(1, self.input_dim[1], input_shape=(self.input_dim[1], 1))(input_reshape)
        conv1d_reshape = tf.reshape(conv1d,[-1,self.input_dim[0]])
        hidden_layer1 = tf.keras.layers.Dense(self.hidden_dim[0],'relu',input_shape=(self.input_dim[0],),use_bias=False)(conv1d_reshape)
        hidden_layer2 = tf.keras.layers.Dense(self.hidden_dim[1],'relu',input_shape=(self.hidden_dim[0],),use_bias=False)(hidden_layer1)
        probs = tf.keras.layers.Dense(self.n_actions, activation='softmax')(hidden_layer2)

        def custom_loss(y_true, y_pred):
          out = K.clip(y_pred, 1e-8, 1-1e-8)
          log_lik = y_true*K.log(out)

          return K.sum(-log_lik*advantages)

        policy = tf.keras.Model(inputs=[input, advantages], outputs=[probs])
        policy.compile(optimizer=tf.keras.optimizers.Adam(lr=self.lr), loss=custom_loss)
        predict = tf.keras.Model(inputs=[input], outputs=[probs])
        print(predict.summary())

        return policy, predict

    def choose_action(self, state):
        probabilities = self.predict.predict(state)[0]
        action = np.random.choice(self.action_space, p=probabilities)
        return action

    def get_probabilities(self, state):
        probabilities = self.predict.predict(state)[0]
        return probabilities

    def store_transition(self, state, action, reward):
        self.state_memory.append(state)
        self.action_memory.append(action)
        self.reward_memory.append(reward)

    def learn(self):
        state_memory = np.array(self.state_memory)
        action_memory = np.array(self.action_memory)
        reward_memory = np.array(self.reward_memory)

        actions = np.zeros([len(action_memory), self.n_actions])
        actions[np.arange(len(action_memory)), action_memory] = 1

        G = np.zeros_like(reward_memory)
        for t in range(len(reward_memory)):
            G_sum = 0
            discount = 1
            for k in range(t, len(reward_memory)):
                G_sum += reward_memory[k] * discount
                discount *= self.gamma
            G[t] = G_sum
        mean = np.mean(G)
        std = np.std(G) if np.std(G) > 0 else 1
        self.G = (G - mean) / std

        cost = self.policy.train_on_batch([state_memory, self.G], actions)

        self.state_memory = []
        self.action_memory = []
        self.reward_memory = []

        return cost

    def learn(self,state_memory,action_memory,reward_memory):
        state_memory = np.array(state_memory)
        action_memory = np.array(action_memory)
        reward_memory = np.array(reward_memory)
        '''
        print('state_memory.shape',state_memory.shape)
        print('action_memory.shape',action_memory.shape)
        print('reward_memory.shape',reward_memory.shape)

        print('len(action_memory)',len(action_memory))
        print('self.n_actions',self.n_actions)
        print('action_memory',action_memory)
        '''

        actions = np.zeros([len(action_memory), self.n_actions])
        actions[np.arange(len(action_memory)), action_memory] = 1

        G = np.zeros_like(reward_memory)
        for t in range(len(reward_memory)):
            G_sum = 0
            discount = 1
            for k in range(t, len(reward_memory)):
                G_sum += reward_memory[k] * discount
                discount *= self.gamma
            G[t] = G_sum
        mean = np.mean(G)
        std = np.std(G) if np.std(G) > 0 else 1
        self.G = (G - mean) / std

        #print('state_memory',state_memory)
        #print('G',G)
        #print('self.G',self.G)
        #print('actions',actions)

        cost = self.policy.train_on_batch([state_memory, self.G], actions)

        #self.state_memory = []
        #self.action_memory = []
        #self.reward_memory = []

        return cost

    def load_weights(self, filename, lastest_num):
        self.policy.load_weights(filename+"_policy_"+str(lastest_num)+".h5")
        self.predict.load_weights(filename+"_predict_"+str(lastest_num)+".h5")

    def load_weights_complete_filename(self, policy_filename, predict_filename):
        self.policy.load_weights(policy_filename)
        self.predict.load_weights(predict_filename)

    def save_weights(self, filename, next_num):
        self.policy.save_weights(filename+"_policy_"+str(next_num)+".h5")
        self.predict.save_weights(filename+"_predict_"+str(next_num)+".h5")
'''

    def __init__ (self, mode = 0, debug = None, input_dim_str = '2', job_cols=1, window_size = 5, hidden_dim_str = '1000,250', node_module=None): # ?
        super(ValueModel, self).__init__()

        self.myInfo = "ValueModel"
        self.debug = debug

        self.job_cols = job_cols
        self.window_size = window_size

        if node_module:
            self.input_dim = [node_module.get_tot()+self.job_cols]
        else:
            self.input_dim = [100+self.job_cols]

        for e in input_dim_str.split(','):
            self.input_dim.append(int(e))

        self.hidden_dim = []

        for e in hidden_dim_str.split(','):
            self.hidden_dim.append(int(e))

        print('input_dim',self.input_dim)
        print('hidden_dim',self.hidden_dim)

        
        
        
        self.debug.line(4," ")
        self.debug.line(4,"#")
        self.debug.debug("# "+self.myInfo,1)
        self.debug.line(4,"#")

        self.conv1d_layer = tf.keras.layers.Conv1D(1, self.input_dim[1], input_shape=(self.input_dim[1], 1))
        # this is our dense hidden layer witha ReLU activiation that will encode most of our information
        self.hidden_layer1 = tf.keras.layers.Dense(self.hidden_dim[0],'relu',input_shape=(self.input_dim[0],),use_bias=False)
        self.hidden_layer2 = tf.keras.layers.Dense(self.hidden_dim[1],'relu',input_shape=(self.hidden_dim[0],),use_bias=False)
        # then we reduce to a single output with a tanh activation
        # we use tanh because -1 <= tanh(x) <= 1 and we will build a reward system based on a range -1 to 1
        self.output_layer = tf.keras.layers.Dense(1,'sigmoid',use_bias=False)

        
        
        #print(self.myInfo)

    def call(self,input):
        # this is the function used to actually evaluate our model on input data
        #print('input',input.shape,input)
        x = tf.reshape(input,[-1,self.input_dim[1],1]) # ?
        #print('input_reshape',x.shape,x)
        x = self.conv1d_layer(x)
        #print('conv1d_layer',x.shape,x)
        x = tf.reshape(x,[-1,self.input_dim[0]]) # ?
        #print('conv1d_reshape',x.shape)
        x = self.hidden_layer1(x)
        #print('hidden_layer1',x.shape)
        x = self.hidden_layer2(x)
        #print('hidden_layer2',x.shape)
        x = self.output_layer(x)
        #print('output_layer',x.shape)
        #print(x)
        return x


# Just quickly look at our model 
test_model = ValueModel() # ?
# in eager execution, we must run the model once to trigger TF to build it
test_model(np.random.rand(2,100+1,2)) # ?
# print a nice summary from Keras
test_model.summary()
# print the trainable parameters
print([x.shape for x in test_model.trainable_variables])
'''
            
            