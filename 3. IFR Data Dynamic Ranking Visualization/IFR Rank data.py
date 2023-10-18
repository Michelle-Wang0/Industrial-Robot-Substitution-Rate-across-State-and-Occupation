# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 13:11:25 2023

@author: 86155
"""
import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML
import matplotlib
matplotlib.rcParams['animation.embed_limit'] = 2**128
def randomcolor():
   colorlist = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
   color =''
   for i in range(6):
       color += random.choice(colorlist)
   return '#'+ color

rank_data=pd.read_csv('IFR Rank data.csv', encoding= 'unicode_escape')
country_set=set(rank_data['Name'])
color_list=[]
for i in range(len(country_set)):
    str_1=randomcolor()
    color_list.append(str_1)
    str_1=randomcolor()
    
country_list=[i for i in country_set]
print(color_list)
print(country_list)

colors=dict(zip(country_list,color_list))
print(colors)

fig,ax=plt.subplots(figsize=(15,8))
def draw_barchart(current_year):
    dff = rank_data[rank_data['Year'].eq(current_year)].sort_values(by='Value',ascending = True).tail(15)
    ax.clear()
    ax.barh(dff['Name'],dff['Value'],color = [colors[x] for x in dff['Name']])
    dx = dff['Value'].max()/100
    for i, (value,name) in enumerate(zip(dff['Value'],dff['Name'])):
       ax.text(value+dx,i ,f'{value:,.0f}',size = 14,ha = 'left',va ='center')
    ax.text(1,0.4,current_year,transform = ax.transAxes,color ='#777777',size = 46,ha ='right',weight=800)
    ax.text(value-dx,i,name,size=20,weight=500,ha ='right',va = 'bottom')
    ax.text(0,1.06,'Robot(Thousand)',transform = ax.transAxes,size=12,color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x',colors='#777777',labelsize=12)
    plt.box(False)
draw_barchart(2018)
animator = animation.FuncAnimation(fig, draw_barchart, frames=range(2011, 2019))
HTML(animator.to_jshtml())
animator.to_html5_video()
animator.save('IFR_rank.mp4')