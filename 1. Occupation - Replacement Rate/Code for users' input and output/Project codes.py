#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This script computes the robot replacement rate for each occupation, 
which we interpret as the possibility of each occupation being replaced by industrial robots.

We use the ONET data which provides an importance score for each skill set for each occupation.

We calculate the replacement rate of each occupation using the sum of scores of the skills 
that will be replaced by industrial robots (physical skills) divided by the sum of score of all the skills required by the occupation.
The higher the rate is, the more likely the occupation will be replaced by robots. 

We also used data from ONET to specify the category each occupation belongs to.
The script as a whole will allow the user to select an occupation to look for by 
first selecting a category, then browse for and select the specific occupation title.

And we will return the replacement rate of that occupation, 
the replacement rate across all occupations,and a bar chart comparing the replacement rate of the selected occpation to the overall average. 

"""


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

file_names = [
    "1.A.1.a.1_Oral Comprehension  Save Table_table.csv",
    "1.A.1.a.2_Written Comprehension  Save Table_table.csv",
    "1.A.1.a.3_Oral Expression  Save Table_table.csv",
    "1.A.1.a.4_Written Expression  Save Table_table.csv",
    "1.A.1.b.1_Fluency of Ideas  Save Table_table.csv",
    "1.A.1.b.2_Originality  Save Table_table.csv",
    "1.A.1.b.3_Problem Sensitivity  Save Table_table.csv",
    "1.A.1.b.4_Deductive Reasoning  Save Table_table.csv",
    "1.A.1.b.5_Inductive Reasoning  Save Table_table.csv",
    "1.A.1.b.6_Information Ordering  Save Table_table.csv",
    "1.A.1.b.7_Category Flexibility  Save Table_table.csv",
    "1.A.1.c.1_Mathematical Reasoning  Save Table_table.csv",
    "1.A.1.c.2_Number Facility  Save Table_table.csv",
    "1.A.1.d.1_Memorization  Save Table_table.csv",
    "1.A.1.e.1_Speed of Closure  Save Table_table.csv",
    "1.A.1.e.2_Flexibility of Closure  Save Table_table.csv",
    "1.A.1.e.3_Perceptual Speed  Save Table_table.csv",
    "1.A.1.f.1_Spatial Orientation  Save Table_table.csv",
    "1.A.1.f.2_Visualization  Save Table_table.csv",
    "1.A.1.g.1_Selective Attention  Save Table_table.csv",
    "1.A.1.g.2_Time Sharing  Save Table_table.csv",
    "1.A.2.a.1_Arm-Hand Steadiness  Save Table_table.csv",
    "1.A.2.a.2_Manual Dexterity  Save Table_table.csv",
    "1.A.2.a.3_Finger Dexterity  Save Table_table.csv",
    "1.A.2.b.1_Control Precision  Save Table_table.csv",
    "1.A.2.b.2_Multilimb Coordination  Save Table_table.csv",
    "1.A.2.b.3_Response Orientation  Save Table_table.csv",
    "1.A.2.b.4_Rate Control  Save Table_table.csv",
    "1.A.2.c.1_Reaction Time  Save Table_table.csv",
    "1.A.2.c.2_Wrist-Finger Speed  Save Table_table.csv",
    "1.A.2.c.3_Speed of Limb Movement  Save Table_table.csv",
    "1.A.3.a.1_Static Strength  Save Table_table.csv",
    "1.A.3.a.2_Explosive Strength  Save Table_table.csv",
    "1.A.3.a.3_Dynamic Strength  Save Table_table.csv",
    "1.A.3.a.4_Trunk Strength  Save Table_table.csv",
    "1.A.3.b.1_Stamina  Save Table_table.csv",
    "1.A.3.c.1_Extent Flexibility  Save Table_table.csv",
    "1.A.3.c.2_Dynamic Flexibility  Save Table_table.csv",
    "1.A.3.c.3_Gross Body Coordination  Save Table_table.csv",
    "1.A.3.c.4_Gross Body Equilibrium  Save Table_table.csv",
    "1.A.4.a.1_Near Vision  Save Table_table.csv",
    "1.A.4.a.2_Far Vision  Save Table_table.csv",
    "1.A.4.a.3_Visual Color Discrimination  Save Table_table.csv",
    "1.A.4.a.4_Night Vision  Save Table_table.csv",
    "1.A.4.a.5_Peripheral Vision  Save Table_table.csv",
    "1.A.4.a.6_Depth Perception  Save Table_table.csv",
    "1.A.4.a.7_Glare Sensitivity  Save Table_table.csv",
    "1.A.4.b.1_Hearing Sensitivity  Save Table_table.csv",
    "1.A.4.b.2_Auditory Attention  Save Table_table.csv",
    "1.A.4.b.3_Sound Localization  Save Table_table.csv",
    "1.A.4.b.4_Speech Recognition  Save Table_table.csv",
    "1.A.4.b.5_Speech Clarity  Save Table_table.csv"
]


list_of_files=[]

# Read csv files into python and change their column names to indicate the skill names 
# Append the 52 csv's columns of interests into a large list

for file in file_names:
    df=pd.read_csv(file)[['Occupation','Importance']]
    skill=file.split('_')[1].replace("  Save Table","")
    df=df.rename(columns={'Importance':skill})
    list_of_files.append(df)


# Merge (inner join) the  files on the shared column 'Occupation':
# With the first file as the base: 

skills_df=list_of_files[0]
for file in list_of_files[1:]:
    skills_df=skills_df.merge(file, on='Occupation', how='inner')


# Min-Max Scaling each column into 0-1 to make the data more uniformed
col_names=skills_df.columns.drop('Occupation')
for col in col_names:
    min=skills_df[col].min()
    max=skills_df[col].max()
    skills_df[col]=(skills_df[col]-min)/(max-min)
    skills_df[col]=skills_df[col].replace(0,0.01)
    


# Calculation Begins:
# Those are the skills that will be replaced by industrial robots (Physical Skills):
replace_col=['Spatial Orientation', 'Visualization', 'Selective Attention', 'Time Sharing', 'Arm-Hand Steadiness', 'Manual Dexterity',
 'Finger Dexterity', 'Control Precision', 'Multilimb Coordination',
 'Response Orientation', 'Rate Control', 'Reaction Time',
 'Wrist-Finger Speed', 'Speed of Limb Movement', 'Static Strength',
 'Explosive Strength', 'Dynamic Strength', 'Trunk Strength', 'Stamina',
 'Extent Flexibility', 'Dynamic Flexibility', 'Gross Body Coordination',
 'Gross Body Equilibrium']

# After sorting out skills that will be replaced,
# we calculate the sum for each occupation:
replaced_df=skills_df[replace_col]
replaced_sum=replaced_df.sum(axis=1)

# Then we use the original df containing all skills to calculate the overall sum:
total_sum=skills_df.drop(columns='Occupation').sum(axis=1)

# making the division to compute replacement rate:
replace_rate=replaced_sum/total_sum

# Making an aggregated df containing the occupation names and its corresponding replacement rate:
agg_df=skills_df[['Occupation']]
agg_df['Score']=replace_rate


# Add the category column to the dataframe 
# This will enable the user to filter the category first, before looking for the specific occupation

# Category informations are recorded and downloaded from ONET in the csv below:
cat_names=[
    "Agriculture_Food_Natural_Resources.csv",
    "Architecture_Construction.csv",
    "Arts_Audio_Video_Technology_Communications.csv",
    "Business_Management_Administration.csv",
    "Education_Training.csv",
    "Finance.csv",
    "Government_Public_Administration.csv",
    "Health_Science.csv",
    "Hospitality_Tourism.csv",
    "Human_Services.csv",
    "Information_Technology.csv",
    "Law_Public_Safety_Corrections_Security.csv",
    "Manufacturing.csv",
    "Marketing.csv",
    "Science_Technology_Engineering_Mathematics.csv",
    "Transportation_Distribution_Logistics.csv"]


# Extracting catrgory names from file names:
# record the corresponding category name of each occupaton:

list_of_cats=[]

for cat in cat_names:
    df=pd.read_csv(cat)[['Occupation']]
    category=cat.split('.')[0].replace("_"," ")
    df['Category']=category
    list_of_cats.append(df)
    


#concatenating those informaton gathered across csv into one data frame:
categories_df=pd.concat(list_of_cats,ignore_index=True)
#categories_df.to_csv('categories.csv',index=False)

# joining the category column to the original data frame 
agg_cat_df=agg_df.merge(categories_df,on='Occupation',how='inner')
#agg_cat_df.to_csv('aggregated with categories.csv',index=False)


# compute a list of category names and the mean of overall replacement rate
# which will be displayed in the user interface:
    
categories=agg_cat_df['Category'].unique()
categories=sorted(categories)
average=agg_cat_df['Score'].mean()
average=round(average*100,2)


# User Interface begins:

while True:
    print("\nWelcome to the replacement possibility checker!\n")
    count=1
    for i in categories:
        print(count,i)
        count+=1
    print("0 Quit")
    while True:
        try:
            cat_num=int(input("Please select the category of your occupation (enter integar): "))
            if cat_num in range (0,len(categories)+1):
                break
            else:
                print('Please make a valid selection\n')  
        except ValueError:
            print('Please enter a valid integar\n')
    if cat_num==0:
        break
    cat=categories[cat_num-1]
    sub_df=agg_cat_df[agg_cat_df['Category']==cat]
    occupations=sub_df['Occupation'].unique()
    occupations=sorted(occupations)
    count=1
    print("")
    for i in occupations:
        print(count,i)
        count+=1
    while True:
        try:
            occ_num=int(input("Please select your occupation (enter integar) or 0 to re-select category: "))
            if occ_num in range (0,len(occupations)+1):
                break
            else:
                print('Please make a valid selection\n')  
        except ValueError:
            print('Please enter a valid integar\n')
    if occ_num==0:
        continue
    occupation=occupations[occ_num-1]
    score=agg_cat_df[agg_cat_df['Occupation']==occupation]['Score'].values[0]
    p=round(score*100,2)
    print("\nThe possibility of",occupation,"being replaced by industrial robots is approximately",p,"%.")
    if p>=average:
        print("\nThis is higher than the average replacement possiblity, which is",average,"%.")
    else:
        print("\nThis is lower than the average replacement possiblity, which is",average,"%.")
    values=[p,average]
    y_pos=np.arange(2)
    labels=[occupation, 'Average']
    plt.bar(y_pos,values)
    plt.xticks(y_pos,labels)
    plt.ylabel("Score")
    plt.ylim(ymin=0,ymax=100)
    plt.show()
    while True:
        try:
            choice=int(input("Enter 1 to start another search, 0 to quit: "))
            if choice in range (0,2):
                break
            else:
                print('Please make a valid selection\n')  
        except ValueError:
            print('Please enter a valid integar\n')
    if choice==1:
        continue
    else:
        break
    
        
    
    
    
    
    
    
    
    
