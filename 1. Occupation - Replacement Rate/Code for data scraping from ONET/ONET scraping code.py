# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 12:21:14 2023

@author: Zhiwen Zhu | Andrew ID: zhiwenz

This .py file is for scrape data from O*NET website to get the skill data for every occupation
First, we iterate over all URLs with occupational skills data in O*NET
Then, we find "table" in website and store them in different csv for the next replacement rate calculation
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
#Iterate over all URLs with occupational skills data in O*NET
#However, not all results have corresponding interfaces, 
#And we'll use try excepts to handle these errors during the crawl.
group1=['1.A.1.g','1.A.1.b','1.A.1.d','1.A.1.e','1.A.1.c','1.A.1.f','1.A.1.a','1.A.3.b','1.A.3.c','1.A.3.a','1.A.2.b','1.A.2.a','1.A.2.c','1.A.4.b','1.A.4.a']
group2=['1','2','3','4','5','6','7']
web=''
weblist=[]
for a in group1:
    for b in group2:
        web=a+'.'+b
        weblist.append(web)
print(weblist)

#Find "table" in website and store them in different csv for the next replacement rate calculation
for i in weblist:
    httpString = 'https://www.onetonline.org/find/descriptor/result/'+i
    print(httpString)
    try:
        page = requests.get(httpString)
        soup = BeautifulSoup(page.content, 'html.parser')
        if page.status_code==200:
            title=soup.find(class_='reportdesc').get_text()
            print(title)
            html_table=soup.find('table')
            table=pd.read_html(str(html_table))
            table=table[0]
            print(table)
            outputname=('%s_%s_table.csv'%(i,title[:-10]))
            table.to_csv(str(outputname))
        else:
            print(f'Page request failed with status code {page.status_code}')
# Using except to handle non-existent pages
    except Exception as e:
        print(f'Page does not exist or an exception occurred：{e}')
