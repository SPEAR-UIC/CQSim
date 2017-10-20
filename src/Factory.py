'''factory'''
import factory_import

__metaclass__ = type

class Module_factory:
    def __init__(self, module_index):
        self.index = module_index
        self.module_list = {}
        self.load_module(factory_import.factory_list)
    
    def load_module(self, modules):
        self.module_list = modules
        
    def filter_job(self, **para):
        return self.module_list[self.index]['f_job'](**para)
        
    def filter_node(self, **para):
        return self.module_list[self.index]['f_node'](**para)
        
    def job(self, **para):
        return self.module_list[self.index]['job'](**para)
        
    def node(self, **para):
        return self.module_list[self.index]['node'](**para)
        
    def backfill(self, **para):
        return self.module_list[self.index]['backfill'](**para)
        
    def start_window(self, **para):
        return self.module_list[self.index]['win'](**para)
        
    def basic_algorithm(self, **para):
        return self.module_list[self.index]['alg'](**para)
        
    def info(self, **para):
        return self.module_list[self.index]['info'](**para)
        
    def cqsim(self, **para):
        return self.module_list[self.index]['sim'](**para)
        
    def debug(self, **para):
        return self.module_list[self.index]['debug'](**para)
    
    def output(self, **para):
        return self.module_list[self.index]['output'](**para)
    