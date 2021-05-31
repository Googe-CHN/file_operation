#-- coding:UTF-8 --
import numpy as np
import os
import json
import argparse

dir_json = '/home/birl/data/manvjie/datasets/training/annotations_json/'
dir_txt = '/home/birl/data/manvjie/datasets/training/annotations_txt/'

def json2txt(path_json,path_txt):
    with open(path_json,'r') as path_json:
        jsonx=json.load(path_json)
        with open(path_txt,'w+') as ftxt:
            for shape in jsonx['shapes']:           
                xy=np.array(shape['points'])
                label=str(shape['label'])
                strxy = ''
                for m,n in xy:
                    strxy+=str(round(m))+','+str(round(n))+','
                strxy+=label
                ftxt.writelines(strxy+"\n") 


if not os.path.exists(dir_txt):
    os.makedirs(dir_txt)
list_json = os.listdir(dir_json)
for cnt,json_name in enumerate(list_json):
    print('cnt=%d,name=%s'%(cnt,json_name))
    path_json = dir_json + json_name
    path_txt = dir_txt + json_name.replace('.json','.txt')
    #print(path_json,path_txt)    
    json2txt(path_json,path_txt)