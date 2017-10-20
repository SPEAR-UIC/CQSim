import IOModule.Log_print as Log_print

__metaclass__ = type

class Debug_log:
    def __init__(self, lvl=2, show=2, path=None):
        self.myInfo = "Debug"
        self.lvl = lvl
        self.path = path
        self.show = show
        self.debugFile=None
        self.debugFile=Log_print.Log_print(self.path,0)
        self.reset_log()
    
    def reset(self, lvl=None, show=None, path=None):
        if lvl:
            self.lvl = lvl
        if show:
            self.show = show
        if path:
            self.path = path
        self.debugFile.reset(self.path,0)
        self.reset_log()
            
    def reset_log(self):
        self.debugFile.reset(self.path,0)
        self.debugFile.file_open()
        self.debugFile.file_close()
        self.debugFile.reset(self.path,1)
        return 1
    
    def set_lvl(self,lvl=0):
        self.lvl = lvl

    def debug(self,context,lvl=3,isEnter=1):
        if (lvl<=self.lvl):
            self.debugFile.file_open()
            self.debugFile.log_print(context,isEnter)
            self.debugFile.file_close()
            if (lvl>=self.show):
                print context
        
    def line(self,lvl=1,signal="-",num=15):
        if (lvl<=self.lvl):
            self.debugFile.file_open()
            i = 0
            context = ""
            while (i<num):
                context += signal
                i += 1
            self.debugFile.log_print(context,1)
            if (lvl>=self.show):
                print context
            self.debugFile.file_close()
    '''
    def start_debug(self):
        self.debugFile.file_open()
        
    def end_debug(self):
        self.debugFile.file_close()
    '''
        