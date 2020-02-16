# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 20:34:24 2019

@author: 78527
"""
import csvFn
import re
import pandas as pd
import math


class JudgeFn:
    def __init__(self):
        pass

    def Seniority(self, Info, seniority):
        '''
        工作经验判断函数,用来判断工作经验是否符合工作年限
        输入工作经验seniority和 Info(DataFrame格式)岗位数据
        返回工作经验大于等于岗位要求的工作年限的Info(DataFrame格式)岗位数据
        '''
        Info = Info.fillna('0')  # 将空白数据填充0
        Info_list = []  # 用来存储索引行号的列表
        if seniority == ' ':
            return Info
        for index, row in Info['job_seniority'].iteritems():  # 遍历表格中的工作年限列表，返回索引和工作年限
            seniorityList = re.findall(r"\d+", row)  # 使用正则表达式取出字符串中第一个连续的数字，最小工作年限
            if seniorityList == []:  # 判断字符串中是否有数字，如果没有 就是没有工作年限的要求
                Info_list.append(index)  # 没有经验要求就直接添加进索引列表
            else:
                # print('index=',index,' 工作年限=',seniorityList[0],'年')#返回工作年限
                if int(seniority) >= int(seniorityList[0]):  # 判断输入的工作经验是否大于等于岗位要求的工作年限
                    Info_list.append(index)  # 将符合条件的岗位索引添加进索引列表
        Info = pd.DataFrame(Info.iloc[Info_list])  # 利用索引列表，取出岗位信息，存储为dataframe格式数据
        return Info.reset_index(drop=True)  # 重建index索引，不然会用原来的索引

    def Seniority_s(self, Info, seniority):
        Info = Info.fillna('0')  # 将空白数据填充0
        Info_list = []  # 用来存储索引行号的列表
        if seniority == ' ':
            return Info
        for index, row in Info['job_seniority'].iteritems():
            if row.find(seniority) + 1:
                Info_list.append(index)
        Info = pd.DataFrame(Info.iloc[Info_list])
        return Info.reset_index(drop=True)  # 重建索引

    def Money(self, Info, money):
        Info = Info.fillna('0')  # 将空白数据填充0
        Info_list = []
        if money == ' ':
            return Info
        for index, row in Info['job_salary'].iteritems():
            if row.find("1.5千以下") + 1:
                row = "1k"
            elif row.find("2万以下") + 1:
                row = "2k"
            elif row.find("100万以上") + 1:
                row = "100k"
            elif row.find("10万以上") + 1:
                row = "10k"
            elif row.find("元/天") + 1:
                pass
            elif row.find("元/小时") + 1:
                pass
            elif row.find("月") + 1:
                if row.find("千") + 1:
                    money_s = re.split("-|千", row)
                    Min_money = money_s[0]
                    row = Min_money + 'k'
                elif row.find("万") + 1:
                    money_s = re.split("-|万", row)
                    Min_money = money_s[0]
                    row = str(float(Min_money) * 10) + 'k'
            elif row.find("年") + 1:
                if row.find("万") + 1:
                    money_s = re.split("-|万", row)
                    Min_money = money_s[0]
                    row = Min_money + 'k'
                moneyList = re.findall(r"\d+", row)  # 最低和最高 统一单位
                # print(row)
                if moneyList == []:
                    Info_list.append(index)
                else:
                    if int(money) <= int(moneyList[0]): Info_list.append(index)
        Info = pd.DataFrame(Info.iloc[Info_list])  # 利用索引列表，取出岗位信息，存储为dataframe格式数据
        return Info.reset_index(drop=True)  # 重建index索引，不然会用原来的索引

    def Edu(self, Info, edu):
        Info = Info.fillna('0')  # 将空白数据填充0
        eduLv = {'初中及以下': '1', '中专': '2', '中技': '2', '高中': '3', '大专': '4', '本科': '5', '硕士': '6', '博士': '7'}
        Info_list = []  # 用来存储索引行号的列表
        edu = eduLv[edu]
        if edu == ' ':
            return Info
        for index, row in Info['job_edu'].iteritems():  # 遍历表格中的学历要求列表，返回索引和学历要求
            if row.find("初中") + 1:
                row = eduLv['初中及以下']
            elif row.find("中专") + 1:
                row = eduLv['中专']
            elif row.find("中技") + 1:
                row = eduLv['中技']
            elif row.find("高中") + 1:
                row = eduLv['高中']
            elif row.find("大专") + 1:
                row = eduLv['大专']
            elif row.find("本科") + 1:
                row = eduLv['本科']
            elif row.find("硕士") + 1:
                row = eduLv['硕士']
            elif row.find("博士") + 1:
                row = eduLv['博士']
            eduList = re.findall(r"\d+", row)
            if eduList == []:
                Info_list.append(index)
            else:
                if int(edu) >= int(eduList[0]):  # 显示比输入Edu小的学历要求
                    Info_list.append(index)
        Info = pd.DataFrame(Info.iloc[Info_list])
        return Info.reset_index(drop=True)  # 重建索引

    def CompanyType(self, Info, Type):
        Info = Info.fillna('0')  # 将空白数据填充0
        Info_list = []  # 用来存储索引行号的列表
        if Type == ' ':
            return Info
        for index, row in Info['company_type'].iteritems():
            if row.find(Type) + 1:
                Info_list.append(index)
        Info = pd.DataFrame(Info.iloc[Info_list])
        return Info.reset_index(drop=True)  # 重建索引

    def CompanySize(self, Info, Size):
        Info = Info.fillna('0')  # 将空白数据填充0
        Info_list = []  # 用来存储索引行号的列表
        if Size == ' ':
            return Info
        for index, row in Info['company_size'].iteritems():
            if row.find(Size) + 1:
                Info_list.append(index)
        Info = pd.DataFrame(Info.iloc[Info_list])
        return Info.reset_index(drop=True)  # 重建索引

    def JobWelfare(self, Info, Welfare):  # 职位待遇
        Info = Info.fillna('0')  # 将空白数据填充0
        Info_list = []  # 用来存储索引行号的列表
        if Welfare == ' ':
            return Info
        for index, row in Info['job_welfare'].iteritems():
            if row.find(Welfare) + 1:
                Info_list.append(index)
        Info = pd.DataFrame(Info.iloc[Info_list])
        return Info.reset_index(drop=True)  # 重建索引

    def JobRequirement():  # 岗位要求
        pass

    def City(self, Info, City):
        Info = Info.fillna('0')  # 将空白数据填充0
        Info_list = []  # 用来存储索引行号的列表
        if City == ' ':
            return Info
        for index, row in Info['city'].iteritems():
            if row.find(City) + 1:
                Info_list.append(index)
        Info = pd.DataFrame(Info.iloc[Info_list])
        return Info.reset_index(drop=True)  # 重建索引

    def Position(self, Info, Position):
        Info = Info.fillna('0')  # 将空白数据填充0
        Info_list = []  # 用来存储索引行号的列表
        if Position == ' ':
            return Info
        for index, row in Info['position'].iteritems():
            if row.find(Position) + 1:
                Info_list.append(index)
        Info = pd.DataFrame(Info.iloc[Info_list])
        return Info.reset_index(drop=True)  # 重建索引


def DataShow(Info, RowNum, Page):  # 输入Info,每页显示多少行,第几页
    StartPg = RowNum * (Page - 1)  # 计算开始行
    EndPg = StartPg + RowNum  # 计算结束行
    PageNum = math.ceil(Info.shape[0] / RowNum)  # 计算一共可以返回多少页
    Info = Info.iloc[StartPg:EndPg]  # 提取信息
    return Info.reset_index(drop=True), PageNum  # 返回信息和一共多少页


if __name__ == '__main__':
    path = r'data.csv'  # 文件打开路径
    Info = csvFn.csvReadFn(path)  # 读取csv
    Judge = JudgeFn()  # 实例化JudgeFn 传入Info
    Info = Judge.Seniority(Info, ' ')  # 传入进来工作经验 字符串类型的数字
    Info=Judge.Money(Info,'8')#传入期望薪资单位为k/月 字符串类型数字
    Info=Judge.Edu(Info,'本科')#传入学历 下拉列表固定值
    Info=Judge.CompanyType(Info,'民营公司')#传入公司类型 下拉列表固定值
    Info=Judge.CompanySize(Info,'50-150人')#传入公司规模 下拉列表固定值
    # Info=Judge.JobWelfare(Info,'五险一金')#传入公司福利 下拉列表固定值
    # Info=Judge.City(Info,'上海')#传入城市
    # Info=Judge.Position(Info,'Python')
    Info, PageNum = DataShow(Info, 9, 3)  # 输入信息和每页显示多少行，第几页
    print(Info, PageNum)