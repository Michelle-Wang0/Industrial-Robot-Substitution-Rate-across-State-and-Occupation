#!/usr/bin/env python
# coding: utf-8

# author: Michelle Wang

"""This script visualizes the robot penetration across states of the USA in a certain year and industry.
 The user can select a year (from 2015, 2016, 2017, or 2018) and an industry (number 1-17),
 then with the Pyecharts library, a geospatial visualizaiton is generated showing each state's robot penetration rate in the input year and industry.
 
 The color on the map reflects the penetration rate – the higher the rate, the warmer the color. 
 This visualization provides a quick overview of how robotics is influencing various industries across different states in the USA.
 The final output is rendered as an HTML file, allowing for easy sharing and viewing."""

# Importing libraries: pandas, pyecharts
import pandas as pd
from pyecharts.charts import Map
from pyecharts.charts import Geo
from pyecharts.datasets import register_url
from pyecharts import options as opts
from pyecharts.globals import ChartType

# Mapping from GeoFips number to state abbreviations
geofips_to_state = {
    "00000": "US",
    "1000": "AL",
    "2000": "AK",
    "4000": "AZ",
    "5000": "AR",
    "6000": "CA",
    "8000": "CO",
    "9000": "CT",
    "10000": "DE",
    "11000": "DC",
    "12000": "FL",
    "13000": "GA",
    "15000": "HI",
    "16000": "ID",
    "17000": "IL",
    "18000": "IN",
    "19000": "IA",
    "20000": "KS",
    "21000": "KY",
    "22000": "LA",
    "23000": "ME",
    "24000": "MD",
    "25000": "MA",
    "26000": "MI",
    "27000": "MN",
    "28000": "MS",
    "29000": "MO",
    "30000": "MT",
    "31000": "NE",
    "32000": "NV",
    "33000": "NH",
    "34000": "NJ",
    "35000": "NM",
    "36000": "NY",
    "37000": "NC",
    "38000": "ND",
    "39000": "OH",
    "40000": "OK",
    "41000": "OR",
    "42000": "PA",
    "44000": "RI",
    "45000": "SC",
    "46000": "SD",
    "47000": "TN",
    "48000": "TX",
    "49000": "UT",
    "50000": "VT",
    "51000": "VA",
    "53000": "WA",
    "54000": "WV",
    "55000": "WI",
    "56000": "WY"
}


""" get_user_input() function:
    Prompt user for year and industry:
        (1) year (str): Chosen year from 2015-2018
        (2) industry (str): Chosen industry from the list with a number
"""
def get_user_input():
    
    # Prompt for year
    while True:
        year = input("Please enter a year (2015, 2016, 2017, 2018): ")
        if year in ["2015", "2016", "2017", "2018"]:
            break
        else:
            print("Invalid year. Try again.")

    # List of industries
    industries = ["agriculture", "automotive", "construction", "electronics", "food", "furniture", 
                  "manufacturing_other", "metal_basic", "metal_machinery", "metal_products", "mineral",
                  "paper", "petrochemicals", "services", "textiles", "utilities", "vehicles_other"]
    
    # Display the industry options with codes
    for idx, ind in enumerate(industries, 1):
        print(f"{idx}. {ind}")

    # Prompt for industry by code
    while True:
        industry_code = input("Please enter an industry code (1 to 17): ")
        if industry_code.isdigit() and 1 <= int(industry_code) <= 17:
            # Convert the industry code back to industry name
            industry = industries[int(industry_code) - 1]
            break
        else:
            print("Invalid industry code. Try again.")

    return year, industry

""" draw_usa_map(title, output_name, normalized_data) function:
    Generates a map visualizing robot penetration across USA, with the input year and industry.
    Parameters:
        (1) title (str): Title of the map.
        (2) output_name (str): Name of the output HTML file.
        (3) normalized_data (list): List of tuples containing state abbreviation and normalized robot penetration rate.
"""
def draw_usa_map(title, output_name, normalized_data):
    try:
        # Register URL that provides map data for various countries
        register_url("https://echarts-maps.github.io/echarts-countries-js/")
    except Exception:
        # If there's an SSL verification issue, bypass it and retry
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        register_url("https://echarts-maps.github.io/echarts-countries-js/")
    
    # Assign normalized_data to list_data
    list_data = normalized_data
    # Getting the maximum value for visual mapping
    max_val = max([item[1] for item in list_data])  
      
    # Initialize the map, set its appearance, and add the coords to the map to show data in points
    # Pyecharts is a library developed by Chinese developers, the maptype="美国" means maptype = 'USA' in English
    geo = (
                Geo(init_opts=opts.InitOpts(width = "1200px", height = "600px", bg_color = '#EEEEE8'))
        .add_schema(maptype="美国",itemstyle_opts=opts.ItemStyleOpts(color="#323c48", border_color="#111"))
        .add_coordinate('WA',-120.04,47.56)
        .add_coordinate('OR',-120.37,43.77)
        .add_coordinate('CA',-120.44,36.44)
        .add_coordinate('AK',-122.00,28.46)
        .add_coordinate('ID',-114.08,43.80)
        .add_coordinate('NV',-116.44,39.61)
        .add_coordinate('MT',-109.42,47.13)
        .add_coordinate('WY',-107.29,42.96)
        .add_coordinate('UT',-111.19,39.35)
        .add_coordinate('AZ',-111.70,34.45)
        .add_coordinate('HI',-105.25,28.72)
        .add_coordinate('CO',-105.52,38.89)
        .add_coordinate('NM',-106.11,34.45)
        .add_coordinate('ND',-100.22,47.53)
        .add_coordinate('SD',-100.52,44.72)
        .add_coordinate('NE',-99.64,41.65)
        .add_coordinate('KS',-98.53,38.43)
        .add_coordinate('OK',-97.13,35.42)
        .add_coordinate('TX',-98.16,31.03)
        .add_coordinate('MN',-94.26,46.02)
        .add_coordinate('IA',-93.60,42.09)
        .add_coordinate('MO',-92.57,38.48)
        .add_coordinate('AR',-92.43,34.69)
        .add_coordinate('LA',-92.49,31.22)
        .add_coordinate('WI',-89.55,44.25)
        .add_coordinate('MI',-84.62,43.98)
        .add_coordinate('IL',-89.11,40.20)
        .add_coordinate('IN',-86.17,40.08)
        .add_coordinate('OH',-82.71,40.31)
        .add_coordinate('KY',-84.92,37.44)
        .add_coordinate('TN',-86.32,35.78)
        .add_coordinate('MS',-89.63,32.66)
        .add_coordinate('AL',-86.68,32.53)
        .add_coordinate('FL',-81.68,28.07)
        .add_coordinate('GA',-83.22,32.59)
        .add_coordinate('SC',-80.65,33.78)
        .add_coordinate('NC',-78.88,35.48)
        .add_coordinate('VA',-78.24,37.48)
        .add_coordinate('WV',-80.63,38.62)
        .add_coordinate('PA',-77.57,40.78)
        .add_coordinate('NY',-75.22,43.06)
        .add_coordinate('MD',-76.29,39.09)
        .add_coordinate('DE',-75.55,39.09)
        .add_coordinate('NJ',-74.47,40.03)
        .add_coordinate('VT',-72.70,44.13)
        .add_coordinate('NH',-71.64,43.59)
        .add_coordinate('MA',-72.09,42.33)
        .add_coordinate('CT',-72.63,41.67)
        .add_coordinate('RI',-71.49,41.64)
        .add_coordinate('ME',-69.06,45.16)
        .add_coordinate('PR',-75.37,26.42)
        .add_coordinate('DC',-77.04,38.90)
        .add("Robot Penetration", list_data, type_=ChartType.EFFECT_SCATTER)
    )  # Add the data as an "Effect Scatter" chart with the label "Robot Penetration"
    
    # Set global options for the map, including the title and visual map options
    geo.set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            visualmap_opts=opts.VisualMapOpts(max_ = max_val, is_piecewise=True),
        )
    # Render the map visualization and save it as file in output_name
    geo.render(output_name)


""" main() function:
    Main function to handle the workflow of the script.
    1. Acquires user input for year and industry with get_user_input()
    2. Filters and processes data, normalize the penetration rate to be more visible in maps
    3. Draws the map visualization with draw_usa_map(title, output_name, normalized_data)
"""
def main():
    # Acquire user input
    year, industry = get_user_input()

    # Load data for the chosen year
    df = pd.read_csv(f"{year}_pene.csv")

    # Filter data by the chosen industry
    filtered_df = df[df["industry_ifr19"] == industry]

    # Extract desired columns
    data = [(geofips_to_state[str(row["GeoFips"])], row["Robot Penetration"]) for _, row in filtered_df.iterrows()]

    # Extract states and their rates
    states, rates = zip(*data)

    # Normalize the rates
    min_rate, max_rate = min(rates), max(rates)
    normalized_rates = [(rate - min_rate) / (max_rate - min_rate) for rate in rates]

    # Combine normalized rates and states
    normalized_data = list(zip(states, normalized_rates))

    # Generate title and output filename based on user's choice
    title = f"Robot Penetration for {industry.capitalize()} in {year}"
    output_name = f"robot_penetration_{year}_{industry}.html"

    # Draw the map
    draw_usa_map(title, output_name, normalized_data)

if __name__ == "__main__":
    main()

