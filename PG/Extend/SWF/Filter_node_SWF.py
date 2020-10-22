import re
import Filter.Filter_node as filter_node

__metaclass__ = type
class Filter_node_SWF(filter_node.Filter_node):
    def reset_config_data(self):
        self.config_start=';'
        self.config_sep='\\n'
        self.config_equal=': '
        self.config_data=[]
        self.config_data.append({'name_config':'MaxNodes','name':'MaxNodes','value':''})
        self.config_data.append({'name_config':'MaxProcs','name':'MaxProcs','value':''})
        
    def read_node_struc(self):
        nr_sign =';'    # Not read sign. Mark the line not the job data
        sep_sign =' '   # The sign seperate data in a line
        sep_sign2 =':'   # The sign seperate data in a line
        nameList=[]
        nameList.append(["MaxNodes","node"])
        nameList.append(["MaxProcs","proc"])
        regex_rest = " *:([^\\n]+)\\n"
        regexList = []
        node_info={}
        
        for dataName in nameList:
            regexList.append([(dataName[0]+regex_rest),dataName[1]])

        nodeFile = open(self.struc,'r')
        while (1):
            tempStr = nodeFile.readline()
            if not tempStr :    # break when no more line
                break
            if tempStr[0] == nr_sign:   # The information line
                for dataRegex in regexList:
                    matchResult = re.findall(dataRegex[0],tempStr)
                    if (matchResult):
                        node_info[dataRegex[1]]=int(matchResult[0].strip())
                        break
                for con_data in self.config_data:
                    con_ex = con_data['name']+self.config_equal+"([^"+self.config_sep+"]*)"+self.config_sep
                    temp_con_List=re.findall(con_ex,tempStr)
                    if (len(temp_con_List)>=1):
                        con_data['value'] = temp_con_List[0]
                        break
            else:
                break
        nodeFile.close()
        self.node_data_build(node_info)
        self.nodeNum = len(self.nodeList)

    def node_data_build(self,node_info):
        node_num = node_info['proc']
        self.nodeList=[]
        i = 0
        while (i < node_num):
            self.nodeList.append({"id": i+1, \
                                  "location": [1], \
                                  "group": 1, \
                                  "state": -1, \
                                  "proc": 1, \
                                  "start": -1, \
                                  "end": -1, \
                                  "extend": None})
            i += 1
        return 1

    def output_node_data(self):
        if not self.save:
            print("Save file not set!")
            return
        
        sep_sign = ";"
        f2=open(self.save,"w")
        for nodeResult_o in self.nodeList:
            f2.write(str(nodeResult_o['id']))
            f2.write(sep_sign)
            f2.write(str(nodeResult_o['location']))
            f2.write(sep_sign)
            f2.write(str(nodeResult_o['group']))
            f2.write(sep_sign)
            f2.write(str(nodeResult_o['state']))
            f2.write(sep_sign)
            f2.write(str(nodeResult_o['proc']))
            f2.write("\n")
        f2.close()

    def output_node_config(self):
        if not self.config:
            print("Config file not set!")
            return
        
        format_equal = '='
        f2=open(self.config,"w")
        
        for con_data in self.config_data:
            f2.write(str(con_data['name_config']))
            f2.write(format_equal)
            f2.write(str(con_data['value']))
            f2.write('\n')
        f2.close()