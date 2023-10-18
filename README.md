# Industrial-Robot-Substitution-Rate-across-State-and-Occupation
## Abstract：
*  Used Pandas to retrieve and clean 70k+ rows of data, including using *API* to fetch U.S. employment data from the Bureau of Economic Analysis (BEA) and *web-scraping* the occupation capabilities data from O*NET Online.
*  Developed metrics to evaluate the regional penetration and occupational replacement rates, established user interfaces for streamlined data querying
*  Employed advanced visualization techniques, including interactive maps with *Pyecharts* and dynamic sorting charts with *Matplotlib Animation*, give users more intuitive illustration of robot penetration with the proliferation of robot use. Over 900+ combinations of charts are available based on user inputs.
   
## Environment: 
Spyder

## Libraries that must be downloaded: 
For the penetration map generation: 
please download the pyecharts in Python: 
* Open Spyder.
* Type `pip install pyecharts`
* Finish! You are ready to run the penetration map generating program.

## For the dynamic ranking: 
please download the ffmpeg on anaconda: 
* Open anaconda prompt.
* Type `conda install -c conda-forge ffmpeg`
* Finish! You are ready to run the dynamic ranking program.

# Program User Instructions
Please unzip the file 'CyberPynk-Final Program.zip'. 

# 1.[Occupational Level Program](https://github.com/Michelle-Wang0/Industrial-Robot-Substitution-Rate-across-State-and-Occupation/tree/aa33a4895888e29dba20fbfd616337cb884a7d9e/1.%20Occupation%20-%20Replacement%20Rate)
## 1.1 Data Scraping:
1. Please open the “1. Occupation - Replacement Rate” folder.
2. After opening the former folder, you will see two folders, please open the “Code for data scraping from ONET” folder for web scraping.
3. The folder should contain the O*NET scraping code py file. Please open it to check the code.
4. If you want to try the scraping, the file will be stored in the same folder with the “ONET scraping code.py”.

## 1.2 Replacement Rate Calculation Instruction:
1. Please open the “1. Occupation - Replacement Rate” folder.
2. After opening the former folder, you will see two folders, please open the “Code for users' input and output” folder.
3. The folder should contain both the py file to be run (Project codes.py) and all the csv files referenced. Please make sure they stay in the same directory (folder) as it is.
4. Please run the py file and follow the instructions on the user interface. The interface prompts for the following inputs: occupation category, occupation title. The output will be the replacement rate of the selected occupation, the average replacement rate across all industries, and a bar chart comparing those two. 


# 2. Regional Level Program
## 2.1 Data retrieving:
1. Please open the “2. Regional - Penetration by States” folder. Then open the “0. Retrieve_BEA_API_data” folder.
2. Download the latest version of BEA-API tool (.whl file) from https://us-bea.github.io/beaapi/README.html
3. You can refer to the detailed instruction from above website to install the BEA-API tool. Open the terminal and type: (The path and the version of the package should convert according to yours)
 `python -m pip install --upgrade --force-reinstall /Users/Your_User_name/Downloads/beaapi-0.0.2-py3-none-any.whl`
4. Register for a BEA-API key in https://apps.bea.gov/api/signup/ and save it to the `beakey = 'YOUR 36-DIGIT API KEY'` in the corresponding part of “Retrieve_BEA_API_data.py”
5. Run the code “Retrieve_BEA_API_data.py” to fetech BEA API data.
6. The retrieved data will be stored in the same folder with the name “201x_employment.xlsx”.

## 2.2 Data cleaning: 
1. Please open the “2. Regional - Penetration by States” folder. Then open the “1. BEA - data cleaning” folder.
2. The folder contains the raw data (before cleaning) and the data cleaning py file (“Data cleaning code 15-18”). Please make sure they stay in the same folder.
3. After running the code, the output CSV will appear in the file as four files named “Penetration_year_for_calculation”. (For your convenience, we put the output files into the file as well, named as “Penetration_year_for_calculation_example” you can check them before running the code if needed.) 

## 2.3 Penetration Rate Calculation:
1. Open the “2. Regional - Penetration by States” folder. Then open the “2. Robot Penetration Calculation” folder.
2. The folder contains the “penetration calculation.py” and cleaned data “Penetration_2015_for_calculate.csv”, as well as the corresponding files for 2016, 2017, and 2018. Keep them in the same folder!
3. Run the .py file. For the input “Enter a state name: ”, enter a state you like with initial capital such as “Ohio”, “New York”. For the input “Enter a year: ”, enter a number between 2015 and 2018. If you enter a wrong name or a state that we did not find related data, it will return “State not found”. And if you enter a year out of range, it will also return “Year not found”.
4. After entering the input, you can get:
   * The robot penetration rate for your input state and year
   * A histogram of the penetration rate of all states for your selected year, with the highlighted bar (in yellow) for your selected state.
   * A line graph comparing the four-year penetration rate for your selected state

## 2.4 Dynamic ranking from 2011-2018
1. Please open the “3. IFR Data Dynamic Ranking Visualization” folder. 
2. The folder contains the data we used for creating the ranking and our .py file.
3. Please download the ffmpeng on anaconda prompt following our instructions in the “libraries that must be downloaded” part.
4. After running the code, the output mp4 will appear in the file as “IFR_rank.mp4” (For your convenience, we put our formal output into the file and adjust its speed as “IFR_rank_adjust_speed.mp4”. You can check that before try the code if needed.)

## 2.5 Interactive Mapping from 2015-2018, 17 industries
1. Please open the “3. Map_Robot_Penetration” folder.
2. The folder contains the data we used for creating the interactive map and our .py file.
3. Run the “map_robot_penetration.py”, after you enter the year and industry in number, the output will appear in the same folder in .html form for convenient sharing and interacting.
4. You can open the .html output externally in your browser (Rightclick and choose “open externnaly” in Spyder; Or click the .html file and you can see a pop up window). Then you can see the interactive map of penetration rate across states for your input year and industry, try to hover your mouse over the data point!

# Files:
## 1. Occupation - Replace Rate File
* 1.1. Code for data scraping from ONET
  * ONET scraping code.p

* 1.2. Code for users’s input and output
  * Project codes.py
  * "1.A.1.a.1_Oral Comprehension  Save Table_table.csv",
    "1.A.1.a.2_Written Comprehension  Save Table_table.csv",
    "1.A.1.a.3_Oral Expression  Save Table_table.csv",
     …
    "1.A.4.b.5_Speech Clarity  Save Table_table.csv"
   
  * "Agriculture_Food_Natural_Resources.csv",
    "Architecture_Construction.csv",
     …
    "Science_Technology_Engineering_Mathematics.csv",
    "Transportation_Distribution_Logistics.csv"

## 2. Regional - Penetration by States
* 2.0. Retrieve_BEA_API_data

* 2.1. BEA - data cleaning
  * Data cleaning code 15-18.py
  * IFR robot data.csv
  * 2015_employment.xlsx ... 2018_employment.xlsx
  * 2010-employment by industry.xlsx
  * 2010-employment by state.xlsx
  * deno code X Industry_Code

* 2.2. Robot Penetration Calculation

* 2.3. Map_Robot_Penetration
  * map_robot_penetration.py
  * 2015_pene.csv ... 2018_pene.csv
