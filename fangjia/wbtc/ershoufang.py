# -*- coding: utf-8 -*-
import csv
import pandas as pd 
import numpy as np 
import re
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Grid
lists=[]
listss=['上海','深圳' ,'北京', '广州', '武汉', '杭州', '南京', '成都', '苏州', '青岛', '长沙', '重庆', '郑州', '合肥', '西安', '大连', '福州', '东莞', '无锡', '厦门', '佛山', '济南', '昆明', '南昌', '天津', '宁波', '沈阳', '珠海', '石家庄', '哈尔滨', '惠州', '常州', '南宁', '昆山', '邯郸', '长春', '贵阳', '太原', '中山', '南通', '温州', '芜湖', '徐州', '乌鲁木齐', '呼和浩特', '嘉兴', '兰州', '海口']
lits=[]
with open('wbtc.csv',encoding='utf-8')as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        lits.append(row[0])
        lits.append(row[1])
        #lits.append(row[2].replace('㎡', '').replace('平方', ''))
        lits.append(row[3].replace('元/㎡', ''))
        lists.append(lits)
        #lits.clear()
        lits=[]
#print(lists)
df = pd.DataFrame(lists,columns=['xx','city','jg'])
df.drop_duplicates(subset=None,keep='first',inplace=True)#去重
df=df.dropna().reset_index(drop=True)
df=df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)#删除缺失
df=df[~df['city'].str.contains('周边')]#删除无用数据
df=df[~df['city'].str.contains('其它|其他')]
#print(df)
for x in listss:#一级城市
    avg_money=[]
    #nn=[]
    city=x
    print(x)
    df1=df[df['city'].str.contains(x+'-')]
    df1=df1.dropna().reset_index(drop=True)
    city_1=df1['city'].str.replace(x+'-','').unique()#去重
    #print(type(df2))
    #print(df2)
    for n in city_1:#二级城市
        df2=df1[df1['city'].str.contains(n)]
        df2['jg']=df2['jg'].astype(float)
        avg_money.append(int(df2['jg'].mean(axis=0)))
        #nn.append(n)
    bar=Bar()

    bar.add_xaxis(list(city_1))
    print(list(city_1))
    bar.add_yaxis("价格 元/㎡", avg_money,color='#d30000',category_gap='40%')
    #bar.reversal_axis()
    bar.set_global_opts(title_opts=opts.TitleOpts(title=x+"二手房价格",subtitle="数据来自58同城",pos_left='center'),
    	       xaxis_opts=opts.AxisOpts(type_='category',axislabel_opts=opts.LabelOpts(interval=0,vertical_align='top',rotate=-45)),
    	       yaxis_opts=opts.AxisOpts(
                name="价格 元/㎡",
                axislabel_opts=opts.LabelOpts(formatter="{value} 元/㎡"),
            ), tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
    	       legend_opts=opts.LegendOpts(pos_left='15%',)
    	       )
    bar.set_series_opts(label_opts=opts.LabelOpts(color="#000000",interval=0))
    bar.render(x+".html")
#def Bar(city_1,avg_money):
    
#datazoom_opts=opts.DataZoomOpts()