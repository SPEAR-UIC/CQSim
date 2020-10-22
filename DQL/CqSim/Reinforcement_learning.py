import random
import numpy as np
import logging,copy,os,sys
from collections import Counter
import tensorflow as tf
#import matplotlib.pyplot as plt
#import IPython.display as ipydis
# turn off all the deprecation warnings
tf.logging.set_verbosity(logging.ERROR)
# turn on eager execution
tf.enable_eager_execution()
tfe = tf.contrib.eager
print('Tensorflow Version: %s',tf.__version__)

__metaclass__ = type

class ValueModel(tf.keras.Model):
    def __init__ (self, mode = 0, debug = None, input_dim_str = '2', job_cols=1, hidden_dim_str = '1000,250', node_module=None, window_size = 5): # ?
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

        
        
        '''
        self.debug.line(4," ")
        self.debug.line(4,"#")
        self.debug.debug("# "+self.myInfo,1)
        self.debug.line(4,"#")
        '''

        self.conv1d_layer = tf.keras.layers.Conv1D(1, self.input_dim[1], input_shape=(self.input_dim[1], 1))
        # this is our dense hidden layer witha ReLU activiation that will encode most of our information
        self.hidden_layer1 = tf.keras.layers.Dense(self.hidden_dim[0],'relu',input_shape=(self.input_dim[0],),use_bias=False)
        self.hidden_layer2 = tf.keras.layers.Dense(self.hidden_dim[1],'relu',input_shape=(self.hidden_dim[0],),use_bias=False)
        # then we reduce to a single output with a tanh activation
        # we use tanh because -1 <= tanh(x) <= 1 and we will build a reward system based on a range -1 to 1
        self.output_layer = tf.keras.layers.Dense(1,'sigmoid',use_bias=False)
        #self.output_layer = tf.keras.layers.Dense(1,'relu',use_bias=False)

        
        
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

'''
# Just quickly look at our model 
test_model = ValueModel() # ?
# in eager execution, we must run the model once to trigger TF to build it
test_model(np.random.rand(2,100+1,2)) # ?
# print a nice summary from Keras
test_model.summary()
# print the trainable parameters
print([x.shape for x in test_model.trainable_variables])
'''

class ForwardAgent():
    def __init__(self,model, weight_fn=None):
        super(ForwardAgent,self).__init__()
        self.myInfo = "ForwardAgent"
        self.model = model

        if weight_fn and os.path.exists(weight_fn):
            print('Loading weights from '+weight_fn)
            self.model.load_weights(weight_fn)
        
        # reset global step
        tf.train.get_or_create_global_step().assign(0)
        
        # for learning rate decay
        # https://towardsdatascience.com/learning-rate-schedules-and-adaptive-learning-rate-methods-for-deep-learning-2c8f433990d1
        self.lr_init = 0.1
        self.decay = tfe.Variable(0.75)
        self.period = tfe.Variable(1.0e5)
        self.lrvar = tfe.Variable(self.lr_init)
  
        self.opt = tf.train.AdamOptimizer()


    # to use LR decay, call this function in your train function
    def learning_rate_update(self):
        lr = self.lr_init * tf.math.pow(self.decay,tf.math.floordiv(tf.cast(self.episode_count,tf.float32),self.period))
        self.lrvar.assign(lr)
  
      # set learning rate decay variables
    def set_lr_init(self,value):
        self.lr_init = value
        self.lrvar.assign(value)
    def set_decay(self,value):
        self.decay.assign(value)
    def set_period(self,value):
        self.period.assign(value)

    def grad(self,inputs):
        # start gradient tape
        with tf.GradientTape() as tape:
          # calculate reward for inputs using model
          value = self.model(inputs)
        # return the reward and the gradients based on this reward
        return value,tape.gradient(value, self.model.trainable_variables)

    def apply_gradients(self,new_grads):
        #print('apply_gradients')
        self.opt.apply_gradients(zip(new_grads, self.model.trainable_variables),global_step=tf.train.get_or_create_global_step())
            
            