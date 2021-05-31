#coding=utf-8
# wirtten by googe, 2018-4-1

# ***有此标志处需要注意修改参数***
#导入模块
import os
import re

#获取输入路径/当前路径
cwd=input('请输入文件路径(结尾加上/)：')  
style_new=input('请输入文件类型(.jpg/.png/.txt/....)：')
# cwd = os.getcwd()

#获取该目录下所有文件，存入列表中
file_ori = os.listdir(cwd)

# ***'[_.]'***
# file_split = [re.split('[_.]', file_single) for file_single in file_ori] # 根据符号'_'和'.'对文件名称进行拆分
file_split = [file_single.split('.') for file_single in file_ori]
num_start = 0

if style_new == '.png':
    #对获取的文件名进行排序,否则是乱序修改
    # ***x[2]*** 注意是第几个参数，把2->
    # _file_sort_ = sorted(file_split, key = lambda x:int(x[2])) # 按照文件中的数字进行排序，确保排序正确
    _file_sort_ = sorted(file_split, key = lambda x:int(x[0]))
    # ***(f[0] + '_' + f[1] + '_')***，注意原名称的命名顺序
    # file_sort = [(f[0] + '_' + f[1] + '_') + f[2] for f in _file_sort_] # 重新将文件名称整合
    file_sort = [f[0] for f in _file_sort_] # 重新将文件名称整合

    n=0
    #遍历修改每一个文件名
    for i in file_sort:
        #获取旧文件名（就是路径+文件名）
        # ***_file_sort_[n][3]***，注意修改对应的位置3->
        oldname = cwd + file_sort[n] + '.' + _file_sort_[n][1]

        #设置新的输出路径和文件名，根据自己的文件名和类型修改
        # output_path = cwd + '/store_folder/'
        # if not os.path.isdir(output_path):
        #     os.mkdir(output_path)

        newname = cwd + '{:07d}'.format(int(num_start)) + style_new # 7位纯数字重命名
    
        #调用rename()重命名函数
        os.rename(oldname,newname)
        #打印修改结果/
        print(oldname,'------->',newname)
        #更新字符串
        n+=1
        num_start +=1
elif style_new == '.json':
    #对获取的文件名进行排序,否则是乱序修改
    # ***x[2]*** 注意是第几个参数，把2->
    # _file_sort_ = sorted(file_split, key = lambda x:int(x[2])) # 按照文件中的数字进行排序，确保排序正确
    _file_sort_ = sorted(file_split, key = lambda x:int(x[0]))
    # ***(f[0] + '_' + f[1] + '_')***，注意原名称的命名顺序
    # file_sort = [(f[0] + '_' + f[1] + '_') + f[2] for f in _file_sort_] # 重新将文件名称整合
    file_sort = [f[0] for f in _file_sort_] # 重新将文件名称整合

    n=0
    #遍历修改每一个文件名
    for i in file_sort:
        #获取旧文件名（就是路径+文件名）
        # ***_file_sort_[n][3]***，注意修改对应的位置3->
        oldname = cwd + file_sort[n] + '.' + _file_sort_[n][1]

        #设置新的输出路径和文件名，根据自己的文件名和类型修改
        # output_path = cwd + '/store_folder/'
        # if not os.path.isdir(output_path):
        #     os.mkdir(output_path)

        newname = cwd + '{:07d}'.format(int(num_start)) + style_new # 7位纯数字重命名
    
        #调用rename()重命名函数
        os.rename(oldname,newname)
        #打印修改结果/
        print(oldname,'------->',newname)
        #更新字符串
        n+=1
        num_start +=1
else:
    #对获取的文件名进行排序,否则是乱序修改
    # ***x[2]*** 注意是第几个参数，把2->
    _file_sort_ = sorted(file_split, key = lambda x:int(x[0])) # 按照文件中的数字进行排序，确保排序正确
    # ***(f[0] + '_' + f[1] + '_')***，注意原名称的命名顺序
    file_sort = [(f[0]) for f in _file_sort_] # 重新将文件名称整合

    n=0
    #遍历修改每一个文件名
    for i in file_sort:
        #获取旧文件名（就是路径+文件名）
        # ***_file_sort_[n][3]***，注意修改对应的位置3->
        oldname = cwd + file_sort[n] + '.' + _file_sort_[n][1]

        #设置新的输出路径和文件名，根据自己的文件名和类型修改
        # output_path = cwd + '/store_folder/'
        # if not os.path.isdir(output_path):
        #     os.mkdir(output_path)

        newname = cwd + '{:07d}'.format(int(num_start)) + style_new # 7位纯数字重命名
    
        #调用rename()重命名函数
        os.rename(oldname,newname)
        #打印修改结果
        print(oldname,'------->',newname)
        #更新字符串
        n+=1
        num_start+=1