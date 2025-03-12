
import os

__metaclass__ = type

class Log_print:
    def __init__(self, filePath, mode=0):
        self.modelist=['w','a']
        self.filePath = filePath
        self.mode = self.modelist[mode]
        self.logFile=None
        self.disabled = False
    
    def reset(self, filePath=None, mode=None):
        if self.disabled:
            return
        if filePath:
            self.filePath = filePath
        if mode:
            self.mode = self.modelist[mode]
        self.logFile=None
    
    def file_open(self):
        if self.disabled:
            return
        self.logFile = open(self.filePath,self.mode)
        return 1
    
    def file_close(self):
        if self.disabled:
            return
        self.logFile.close()
        return 1
    
    def log_print(self, context, isEnter=1):
        if self.disabled:
            return
        self.logFile.write(str(context))
        if isEnter==1:
            self.logFile.write("\n")

    def disable(self):
        self.disabled = True

    
            
        