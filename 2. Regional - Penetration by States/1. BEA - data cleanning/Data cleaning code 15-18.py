# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 20:56:36 2023

@author: Zhiwen Zhu | andrew ID: zhiwenz
"""
'''
This script is for matching and cleaning the data set we collected:
1. industry robots stock data of US from IFR (from 2015-2018),
2. Census data of employment in 2010 by industry (base time)
3. Census data of employment in 2010 by state
4. Employment data by state and industry from BEA of 2015-2018

First, those 4 data use different industry category codes. Thus we first match the data 
with the 2010 census data code and create 2 CSV files to match the category. 
We match the robot data and the BEA data with the new category code and group by the new category code separately.

Second, we merge the IFR robot data and the BEA data using the industry category code. 

Third, we merge the merged IFR and BEA data with the census employment data by state using state code, 
and we merge the merged data with the census employment data by industry using industry category code.

The outputs divided into 4 separate CSV files from 2015 to 2018 that ready to compute directly.
'''
import pandas as pd
#Step 1: Match the IFR's industry classification code with the industry classification code used in the calculation
    #Importing csv data into a dataframe
robot_raw=pd.read_csv('IFR robot data.csv')
ifr_to_deno=pd.read_excel('IFR-deno.xlsx')
    #Delete the empty data
robot_raw.dropna(inplace=True)

    #Year 2015 - match the IFR industry classicication code with the calculation classification (deno code)
condition=robot_raw['year']==2015
robot_2015=robot_raw[condition]
robot_2015_deno=pd.merge(robot_2015,ifr_to_deno,on='industry name',how='inner')
robot_2015_deno=robot_2015_deno.groupby('deno code',as_index=False)['U.S robot data'].sum()
print(robot_2015_deno)
    #Year 2016 - match the IFR industry classicication code with the calculation classification (deno code)
condition=robot_raw['year']==2016
robot_2016=robot_raw[condition]
robot_2016_deno=pd.merge(robot_2016,ifr_to_deno,on='industry name',how='inner')
robot_2016_deno=robot_2016_deno.groupby('deno code',as_index=False)['U.S robot data'].sum()
print(robot_2016_deno)
    #Year 2017 - match the IFR industry classicication code with the calculation classification (deno code)
condition=robot_raw['year']==2017
robot_2017=robot_raw[condition]
robot_2017_deno=pd.merge(robot_2017,ifr_to_deno,on='industry name',how='inner')
robot_2017_deno=robot_2017_deno.groupby('deno code',as_index=False)['U.S robot data'].sum()
print(robot_2017_deno)
    #Year 2018 - match the IFR industry classicication code with the calculation classification (deno code)
condition=robot_raw['year']==2018
robot_2018=robot_raw[condition]
robot_2018_deno=pd.merge(robot_2018,ifr_to_deno,on='industry name',how='inner')
robot_2018_deno=robot_2018_deno.groupby('deno code',as_index=False)['U.S robot data'].sum()
print(robot_2018_deno)

#Step 2: Match the U.S. Bureau of Economic Analysis (BEA) data (employment by industry and state) with the industry classification code used in the calculation.
    #Transform the excel data we scrape from BEA to DataFrame
bea_to_deno=pd.read_excel('deno code X Industry_Code.xlsx')
employ_2015=pd.read_excel('2015_employment.xlsx')
employ_2016=pd.read_excel('2016_employment.xlsx')
employ_2017=pd.read_excel('2017_employment.xlsx')
employ_2018=pd.read_excel('2018_employment.xlsx')
    
    #Match the employ code used in BEA with our calculation industry code (deno code)
employ_2015_deno=pd.merge(employ_2015,bea_to_deno,on='occupation',how='inner')
employ_2016_deno=pd.merge(employ_2016,bea_to_deno,on='occupation',how='inner')
employ_2017_deno=pd.merge(employ_2017,bea_to_deno,on='occupation',how='inner')
employ_2018_deno=pd.merge(employ_2018,bea_to_deno,on='occupation',how='inner')

    #Drop the missing value (When the employment is 0)
employ_2015_deno=employ_2015_deno.drop(employ_2015_deno[employ_2015_deno['DataValue']==0].index)
employ_2016_deno=employ_2016_deno.drop(employ_2016_deno[employ_2016_deno['DataValue']==0].index)
employ_2017_deno=employ_2017_deno.drop(employ_2017_deno[employ_2017_deno['DataValue']==0].index)
employ_2018_deno=employ_2018_deno.drop(employ_2018_deno[employ_2018_deno['DataValue']==0].index)

    #Group by states code and our calculation industry code (deno code) and then count the sum
employ_2015_deno=employ_2015_deno.groupby(['GeoFips','GeoName','deno code'],as_index=False)['DataValue'].sum()
employ_2016_deno=employ_2016_deno.groupby(['GeoFips','GeoName','deno code'],as_index=False)['DataValue'].sum()
employ_2017_deno=employ_2017_deno.groupby(['GeoFips','GeoName','deno code'],as_index=False)['DataValue'].sum()
employ_2018_deno=employ_2018_deno.groupby(['GeoFips','GeoName','deno code'],as_index=False)['DataValue'].sum()

#Step 3: Match the data of base period (employment in 2010) and the IFR robot data with the BEA employment data for each year
    #Importing excel data into a DataFrame
emp2010=pd.read_excel('2010-employment by state.xlsx')
empbyind2010=pd.read_excel('2010-employment by industry.xlsx')
emp2010=emp2010.rename(columns={'emloyment population ':'employment population'})

    #2015 BEA Employment Data Match with the 2010 employment data and the IFR robot data
    #Then Export a csv that can be calculated directly
employ_2015_deno=pd.merge(employ_2015_deno,robot_2015_deno,on='deno code',how='inner')
employ_2015_deno=pd.merge(employ_2015_deno,empbyind2010,on='deno code',how='inner')
employ_2015_deno=pd.merge(employ_2015_deno,emp2010,on='GeoName',how='inner')
employ_2015_deno=employ_2015_deno.rename(columns={'DataValue':'2015 employment by industry',
                                                  'employment population':'2010employment by state',
                                                  'U.S robot data':'2015 robot data'})
print(employ_2015_deno)
employ_2015_deno.to_csv('Penetration_2015_for_calculate.csv',index=False)

    #2016 BEA Employment Data Match with the 2010 employment data and the IFR robot data
    #Then Export a csv that can be calculated directly
employ_2016_deno=pd.merge(employ_2016_deno,robot_2016_deno,on='deno code',how='inner')
employ_2016_deno=pd.merge(employ_2016_deno,empbyind2010,on='deno code',how='inner')
employ_2016_deno=pd.merge(employ_2016_deno,emp2010,on='GeoName',how='inner')
employ_2016_deno=employ_2016_deno.rename(columns={'DataValue':'2016 employment by industry',
                                                  'employment population':'2010employment by state',
                                                  'U.S robot data':'2016 robot data'})
print(employ_2016_deno)
employ_2016_deno.to_csv('Penetration_2016_for_calculate.csv',index=False)

    #2017 BEA Employment Data Match with the 2010 employment data and the IFR robot data
    #Then Export a csv that can be calculated directly
employ_2017_deno=pd.merge(employ_2017_deno,robot_2017_deno,on='deno code',how='inner')
employ_2017_deno=pd.merge(employ_2017_deno,empbyind2010,on='deno code',how='inner')
employ_2017_deno=pd.merge(employ_2017_deno,emp2010,on='GeoName',how='inner')
employ_2017_deno=employ_2017_deno.rename(columns={'DataValue':'2017 employment by industry',
                                                  'employment population':'2010employment by state',
                                                  'U.S robot data':'2017 robot data'})
print(employ_2017_deno)
employ_2017_deno.to_csv('Penetration_2017_for_calculate.csv',index=False)

    #2018 BEA Employment Data Match with the 2010 employment data and the IFR robot data
    #Then Export a csv that can be calculated directly
employ_2018_deno=pd.merge(employ_2018_deno,robot_2018_deno,on='deno code',how='inner')
employ_2018_deno=pd.merge(employ_2018_deno,empbyind2010,on='deno code',how='inner')
employ_2018_deno=pd.merge(employ_2018_deno,emp2010,on='GeoName',how='inner')
employ_2018_deno=employ_2018_deno.rename(columns={'DataValue':'2018 employment by industry',
                                                  'employment population':'2010employment by state',
                                                  'U.S robot data':'2018 robot data'})
print(employ_2018_deno)
employ_2018_deno.to_csv('Penetration_2018_for_calculate.csv',index=False)