# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 10:37:04 2019

@author: 78527
"""

import pandas as pd
#import re

def csvReadFn(path):
    '''
    输入path路径，读取csv，返回csv的DataFrame
    
    数据类型：
    position    object
    company     object
    city        object
    money       object
    data        object
    job_msg     object
    dtype: object
    
    调用的时候直接用调用字典的用法
    例如：
    Info=csvReadfn(r'InfoTest_100.csv')
    输出第10条数据的城市 print(Info['city'][10])
    输出城市列表 print(Info['city'])
    
    详细查阅pandas的DataFrame数据类型用法
    https://blog.csdn.net/daydayup_668819/article/details/82315565
    '''
    data = pd.read_csv(path,encoding='utf-8',error_bad_lines = False)  # 读取csv
    Info=pd.DataFrame(data)
    
    return Info
def csvWriteFn(path,Info):
    '''
    输入path路径和DataFrame类型的Info，保存为csv，返回是否成功
    csvWrite(outpath,Info)
    '''
    writeInfo=[]
    writeInfo.append(Info)
    try:
        pd.concat(writeInfo, ignore_index=True).to_csv(path,index=False,sep=',',mode='a+',encoding='utf-8')
    except:
        print('  尝试追加到CSV失败')
    else:
        print('  追加CSV内容成功')


if __name__=='__main__':
    path=r'InfoTest_101.csv'
    outpath=r'InfoTest_103.csv'
    Info=csvReadFn(path)
    csvWriteFn(outpath,Info)
    
    #print(Info.head(5).values)#Numpy的展示方式  前5行
    pass