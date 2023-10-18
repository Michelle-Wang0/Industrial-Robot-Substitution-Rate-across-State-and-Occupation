#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt


'''
This script computes the robot penetration rate for each state in the U.S. over a span of four years,
and calculates the robot penetration rate for each industry of each state in a specific year.
We've also created a user interface that allows users to input a state name and year simultaneously.
Upon entry, the user will receive the penetration rate for that specific state and year, a chart comparing the robot penetration of that state with others for the selected year,
and a comparison of the robot penetration for the state over the four-year period.
'''


#read csv file

data1 = pd.read_csv('Penetration_2015_for_calculate.csv')
data2 = pd.read_csv('Penetration_2016_for_calculate.csv')
data3 = pd.read_csv('Penetration_2017_for_calculate.csv')
data4 = pd.read_csv('Penetration_2018_for_calculate.csv')

# Calculate robot penetration for each industry
data1['Robot Penetration'] = (data1['2015 employment by industry'] / data1['2010employment by state']) * \
                            (data1['2015 robot data'] / data1['2010 employment by industry'])
data2['Robot Penetration'] = (data2['2016 employment by industry'] / data2['2010employment by state']) * \
                            (data2['2016 robot data'] / data2['2010 employment by industry'])
data3['Robot Penetration'] = (data3['2017 employment by industry'] / data3['2010employment by state']) * \
                            (data3['2017 robot data'] / data3['2010 employment by industry'])
data4['Robot Penetration'] = (data4['2018 employment by industry'] / data4['2010employment by state']) * \
                            (data4['2018 robot data'] / data4['2010 employment by industry'])
                            

# Display the updated dataset with the Robot Penetration column

print(data1[['GeoName', 'industry_ifr19', 'Robot Penetration']])
print(data2[['GeoName', 'industry_ifr19', 'Robot Penetration']])
print(data3[['GeoName', 'industry_ifr19', 'Robot Penetration']])
print(data4[['GeoName', 'industry_ifr19', 'Robot Penetration']])

# Calculate the robot penetration for each state by summing up the robot penetration of each industry within that state
state_penetration_2015 = data1.groupby('GeoName')['Robot Penetration'].sum().reset_index()

# Display the robot penetration for each state for year 2015
print('2015 Robot Penetration by State:')
print(state_penetration_2015)

# Calculate the robot penetration for each state by summing up the robot penetration of each industry within that state
state_penetration_2016 = data2.groupby('GeoName')['Robot Penetration'].sum().reset_index()

# Display the robot penetration for each state for year 2016
print('2016 Robot Penetration by State:')
print(state_penetration_2016)

# Calculate the robot penetration for each state by summing up the robot penetration of each industry within that state
state_penetration_2017 = data3.groupby('GeoName')['Robot Penetration'].sum().reset_index()

# Display the robot penetration for each state for year 2017
print('2017 Robot Penetration by State:')
print(state_penetration_2017)

# Calculate the robot penetration for each state by summing up the robot penetration of each industry within that state
state_penetration_2018 = data4.groupby('GeoName')['Robot Penetration'].sum().reset_index()

# Display the robot penetration for each state for year 2018
print('2018 Robot Penetration by State:')
print(state_penetration_2018)


#Plotting the histogram of Robot Penetration by State for year 2015
state_penetration_2015_sorted = state_penetration_2015.sort_values(by = 'Robot Penetration', ascending = True)
plt.figure(figsize = (15, 10))
plt.bar(state_penetration_2015_sorted['GeoName'], state_penetration_2015_sorted['Robot Penetration'])
plt.title('Robot Penetration by State 2015')
plt.xlabel('State')
plt.ylabel('Robot Penetration')
plt.xticks(rotation = 90, fontsize = 7)

#Plotting the histogram of Robot Penetration by State for year 2016
state_penetration_2016_sorted = state_penetration_2016.sort_values(by = 'Robot Penetration', ascending = True)
plt.figure(figsize = (15, 10))
plt.bar(state_penetration_2016_sorted['GeoName'], state_penetration_2016_sorted['Robot Penetration'])
plt.title('Robot Penetration by State 2016')
plt.xlabel('State')
plt.ylabel('Robot Penetration')
plt.xticks(rotation = 90, fontsize = 7)

#Plotting the histogram of Robot Penetration by State for year 2017
state_penetration_2017_sorted = state_penetration_2017.sort_values(by = 'Robot Penetration', ascending = True)
plt.figure(figsize = (15, 10))
plt.bar(state_penetration_2017_sorted['GeoName'], state_penetration_2017_sorted['Robot Penetration'])
plt.title('Robot Penetration by State 2017')
plt.xlabel('State')
plt.ylabel('Robot Penetration')
plt.xticks(rotation = 90, fontsize = 7)

#Plotting the histogram of Robot Penetration by State for year 2018
state_penetration_2018_sorted = state_penetration_2018.sort_values(by = 'Robot Penetration', ascending = True)
plt.figure(figsize = (15, 10))
plt.bar(state_penetration_2018_sorted['GeoName'], state_penetration_2018_sorted['Robot Penetration'])
plt.title('Robot Penetration by State 2018')
plt.xlabel('State')
plt.ylabel('Robot Penetration')
plt.xticks(rotation = 90, fontsize = 7)
plt.show()


#Creating a list for positioning the correct Robot Penetration by State by year histogram later 
state_penetration = []
state_penetration.append(state_penetration_2015)
state_penetration.append(state_penetration_2016)
state_penetration.append(state_penetration_2017)
state_penetration.append(state_penetration_2018)


#Prompt function
def get_state_penetration(state_input, year):
    if year == '2015':
        pene_value = state_penetration_2015[state_penetration_2015['GeoName'] == state_input]['Robot Penetration'].values
    elif year == '2016':
        pene_value = state_penetration_2016[state_penetration_2015['GeoName'] == state_input]['Robot Penetration'].values
    elif year == '2017':
        pene_value = state_penetration_2017[state_penetration_2015['GeoName'] == state_input]['Robot Penetration'].values
    elif year == '2018':
        pene_value = state_penetration_2018[state_penetration_2015['GeoName'] == state_input]['Robot Penetration'].values
    else:
        return 'Year not found'
        
    if pene_value.size > 0:
        return pene_value[0]
    else:
        return 'State not found'


#Prompt the user to enter a state name and a year to get the information they need
#User input requirement needed: please enter a state name with initial capital, such as Ohio.
while True:
    state_input = input("Enter a state name (or type 'quit' to exit): ")
    year = input("Enter a year (or type 'quit' to exit): ")
    if state_input == 'quit' or year == 'quit':
        break
    pene_value = get_state_penetration(state_input, year)
    if isinstance(pene_value, str):
        print(pene_value)
    else:
        print(f'{year} Robot penetration for {state_input}: {pene_value:.4f}')
     
        #Retunring the specific year of histogram graph, and highlight the penetration bar of the specific state
        state = state_penetration[int(year) - 2015]  #Positioning correct year of histogram graph
        state_penetration_sorted = state.sort_values(by = 'Robot Penetration', ascending = True)
        colors = ['y' if i == state_input else 'blue' for i in state_penetration_sorted['GeoName']]
        plt.figure(figsize = (13, 5))
        plt.bar(state_penetration_sorted['GeoName'], state_penetration_sorted['Robot Penetration'], color=colors)
        plt.title(f'Robot Penetration by State {year}')
        plt.xlabel('State')
        plt.ylabel('Robot Penetration')
        plt.xticks(rotation = 90, fontsize = 7)
        plt.show()
        plt.pause(1)
        
        #Getting specific year and state penetration rate
        pene_list = []
        pene_value1 = state_penetration_2015[state_penetration_2015['GeoName'] == state_input]['Robot Penetration'].values
        pene_value2 = state_penetration_2016[state_penetration_2016['GeoName'] == state_input]['Robot Penetration'].values
        pene_value3 = state_penetration_2017[state_penetration_2017['GeoName'] == state_input]['Robot Penetration'].values
        pene_value4 = state_penetration_2018[state_penetration_2018['GeoName'] == state_input]['Robot Penetration'].values
        pene_list.append(pene_value1)
        pene_list.append(pene_value2)
        pene_list.append(pene_value3)
        pene_list.append(pene_value4)    
        years = [2015, 2016, 2017, 2018]
        
        #Returning the specific four-year Robot penetration comparison line graph
        plt.figure(figsize = (12, 5))
        plt.plot(years, pene_list)
        plt.title(f'{state_input} Four-year Robot Penetration')
        plt.xlabel('Year')
        plt.ylabel('Robot Penetration')
        plt.xticks(range(2015,2019))
        for i_x, i_y in zip(years, pene_list):
            rounded_i_y = round(i_y[0], 3)
            plt.text(i_x, rounded_i_y, '({}, {})'.format(i_x, rounded_i_y))
        plt.show()
        plt.pause(1)
    





