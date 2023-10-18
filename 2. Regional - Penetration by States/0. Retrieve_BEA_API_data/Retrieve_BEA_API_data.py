#!/usr/bin/env python
# coding: utf-8
# Michelle Wang

""" After downloading BEA-API from https://us-bea.github.io/beaapi/README.html
we can open the terminal and type:  python -m pip install --upgrade --force-reinstall /Users/manqiaowang/Downloads/beaapi-0.0.2-py3-none-any.whl 
Note that the path and the version of the package should convert according to yours! """

""" We use the following script to fetch and organize employment data from the Bureau of Economic Analysis (BEA)'s API,
   in order to further compute the robot penetration rate for industries in each state across each year.
   Then we can provide the user with a 5-year trend penetration rate chart, a dynamic ranking of the State's penetration rate, and a nationwide map of penetration rate for a certain industry.
 
 The BEA provides an enormous amount of data with multiple datasets/tables, we first probe into the structure of the data, fetching a list of tables, parameters, geographic FIPS codes (GeoFips), and industry line codes
 Our focus is the 'Regional' dataset, and we look into the "SAEMP25N-Total full-time and part-time employment by NAICS industry" table inside it."""

"""Then, we can retrieve employment data for *industries* in different *states* across different *years*.
There are 3 dimensions of data, so we loop through years, industries, and states to retrieve the data.
The industries are from Occupation_Code.xlsx, which are data we filtered using the Regional_LineCode.xlsx, in order to match the industry data in our other data source.
The states are from Regional_GeoFip.xlsx, we filtered only states (codes end in 000) from all the GeoFip codes. 
Then the data is saved into Excel for further calculation. """

# Import libraries/modules
import beaapi  # Module for accessing BEA (Bureau of Economic Analysis) data through API
import pandas as pd  # Library for data manipulation and analysis

# Set the BEA API key
beakey = 'EB090666-4F3D-4DD1-9596-EE68BA4DD36B'
# you can get this key from BEA official website

#### Probing into Data ####

# 1. Preparation: Understanding structure of the available BEA data
# 1.(1) Obtain a list of datasets available from the BEA API
list_of_sets = beaapi.get_data_set_list(beakey)
print('(1)list_of_tables', list_of_sets)  

# 1.(2) Obtain a list of parameters for accessing a specific dataset ('Regional' in this case)
list_of_params = beaapi.get_parameter_list(beakey, 'Regional')
print('(2)list_of_params', list_of_params) 

# 1.(3) Dive deeper into the 'Regional' dataset and get a list of available table names
list_of_param_vals = beaapi.get_parameter_values(beakey, 'Regional', 'TableName')
print('(3)Regional_TableName', list_of_param_vals)  
# After exploring each table, we know that "SAEMP25N-Total full-time and part-time employment by NAICS industry" will serve our needs.

# 1.(4) Obtain the geographic FIPS codes (GeoFips) which include state codes
geo_fips = beaapi.get_parameter_values(beakey, 'Regional', 'GeoFips')
print('(4)Geo_Fips',geo_fips.head(5))

# Save the GeoFips codes to an Excel file for future reference
df = pd.DataFrame(geo_fips)
filename = 'Regional_GeoFip_origin.xlsx'
df.to_excel(filename, index=False)

# 1.(5) Obtain the industry line codes under the 'Regional' dataset
list_of_param_vals = beaapi.get_parameter_values(beakey, 'Regional', 'LineCode')
print('(5)Regional_LineCode',list_of_param_vals.head(5)) 
# There are linecodes indicating the industry employment, such as "[SAEMP25N] Private nonfarm employment: Construction (23)","[SAEMP25N] Private nonfarm employment: Educational services (61)"

# Save the line codes to an Excel file for future reference
df = pd.DataFrame(list_of_param_vals)
filename = 'Regional_LineCode.xlsx'
df.to_excel(filename, index=False)

#### Retrieving Data ####

# Load occupation codes and geographic FIPS codes from Excel files
occupation_codes = pd.read_excel('Occupation_Code.xlsx', dtype=str)
geo_fips = pd.read_excel('Regional_GeoFip.xlsx', dtype=str)

# Convert the loaded Excel data to lists for iteration
occupation_list = occupation_codes.iloc[:, 0].tolist()
state_list = geo_fips.iloc[:, 0].tolist()

# Define the range of years for which data needs to be fetched
years = list(range(2015, 2021))

# Calculate total workload for progress tracking
total_workload = len(years) * len(occupation_list) * len(state_list)
completed_work = 0

# Loop through years, occupations, and states to fetch and process data
for year in years:
    states = pd.DataFrame()  # DataFrame to store data for each year
    for occupation in occupation_list:
        for state in state_list:
            # Construct a unique code based on occupation for fetching data
            code = f"SAEMP25N-{occupation}"
            try:
                # beaapi.get_data(): Retrieve data from BEA using API 
                bea_tbl = beaapi.get_data(beakey, datasetname='Regional', TableName='SAEMP25N', GeoFips=state, Year=str(year), LineCode=str(occupation))
                bea_tbl['occupation'] = occupation
                states = pd.concat([states, bea_tbl], ignore_index=True)
                data1 = {'Code': [code],'GeoFips': [state],  'TimePeriod': [year]}
                print('Ready----',data1)
                
            except Exception as e:
                # Handle exceptions (if the API returns an internal error)
                if "Internal API error retrieving data" in str(e):
                    # Create a default error entry to be added to the DataFrame
                    error_data = {
                        'Code': [code],
                        'GeoFips': [state],
                        'GeoName': [None],  # or 'Unknown'
                        'TimePeriod': [year],
                        'CL_UNIT': ['Number of jobs'],
                        'UNIT_MULT': [0],
                        'DataValue': [0],
                        'occupation': [occupation]
                    }
                    print('Not valid',error_data)
                    states = pd.concat([states, pd.DataFrame(error_data)], ignore_index=True)

            
    # Save the data for the current year to an Excel file
    output_filename = f"{year}_employment.xlsx"
    states.to_excel(output_filename, index=False)




