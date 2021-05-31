#coding=utf-8
## 功能：批量处理文件，对其中逆序排列的boundingbox顶点进行顺时针处理，第一点为图片中的左上点
import os
import numpy as np

# 获取列表的第二个元素
def takeSecond(elem):
    return elem[1]

#获取输入路径/当前路径
# cwd = input("请输入文件路径(结尾加上/)：")  
cwd = '/home/birl/climbingrobot_ws/src/data_operation/generate_JSON/p9/training/p5_training_annotation/'

#获取该目录下所有文件，存入列表中
file_ori = os.listdir(cwd)

file_split = [file_single.split('.') for file_single in file_ori]# 根据符号'.'对文件名称进行拆分

#对获取的文件名进行排序,否则是乱序修改
_file_sort_ = sorted(file_split, key = lambda x:int(x[0])) # 按照文件中的数字进行排序，确保排序正确
file_sort = [f[0] for f in _file_sort_] # 重新将文件名称整合

n = 0
#遍历修改每一个文件名
for i in file_sort:
    #获取旧文件名（就是路径+文件名）
    oldname = cwd + file_sort[n] + '.' + _file_sort_[n][1]

    file_modified = open(oldname)
    file_data = ""
    for fi in file_modified.readlines():
        current_line = fi.strip().split(',')
        # print('current_line \n', current_line)
        bbx =  [
                    [int(float(current_line[0])), int(float(current_line[1]))],
                    [int(float(current_line[2])), int(float(current_line[3]))],
                    [int(float(current_line[4])), int(float(current_line[5]))],
                    [int(float(current_line[6])), int(float(current_line[7]))]
                ]
        
        edge =  [
                    ( bbx[1][0] - bbx[0][0])*( bbx[1][1] + bbx[0][1]),
                    ( bbx[2][0] - bbx[1][0])*( bbx[2][1] + bbx[1][1]),
                    ( bbx[3][0] - bbx[2][0])*( bbx[3][1] + bbx[2][1]),
                    ( bbx[0][0] - bbx[3][0])*( bbx[0][1] + bbx[3][1])
                ]
    
        summatory = edge[0] + edge[1] + edge[2] + edge[3]
        
        if summatory > 0:
            current_line = str(bbx[1][0]) + ',' + str(bbx[1][1]) + ',' + str(bbx[0][0]) + ',' + str(bbx[0][1]) \
                            + ',' + str(bbx[3][0]) + ',' + str(bbx[3][1]) + ',' + str(bbx[2][0]) + ',' + str(bbx[2][1]) + ',pole\n'

            fi = fi.replace(fi, current_line)
            # print('fi \n', fi)
            file_data += fi
        else:
            current_line = str(bbx[0][0]) + ',' + str(bbx[0][1]) + ',' + str(bbx[1][0]) + ',' + str(bbx[1][1]) \
                            + ',' + str(bbx[2][0]) + ',' + str(bbx[2][1]) + ',' + str(bbx[3][0]) + ',' + str(bbx[3][1]) + ',pole\n'
            fi = fi.replace(fi, current_line)
            file_data += fi

    #设置新的输出路径和文件名，根据自己的文件名和类型修改
    output_path = cwd + '/store_folder/'
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    # newname = cwd + '{:07d}'.format(int(n)) + style_new # 7位纯数字重命名
    newname = output_path + file_sort[n] + '.' + _file_sort_[n][1] # 保留原名称保存于当前路径下的‘store_folder’下

    file_new = open(newname, 'w')
    file_new.write(file_data)
    file_new.close()
    file_modified.close()

    #打印修改结果
    print(oldname,'------->',newname)
    n += 1