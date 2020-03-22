#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Libraries" data-toc-modified-id="Libraries-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Libraries</a></span></li><li><span><a href="#Initialize-configuration" data-toc-modified-id="Initialize-configuration-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Initialize configuration</a></span></li><li><span><a href="#Functions" data-toc-modified-id="Functions-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Functions</a></span></li><li><span><a href="#Main" data-toc-modified-id="Main-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Main</a></span></li></ul></div>

# # Libraries

# In[1]:


import pandas as pd # library for data analsysis
import requests # library to handle requests
import plotly.express as px # library to plot on map
import matplotlib.pyplot as plt # library to plot
from bs4 import BeautifulSoup # library to handle sitmaps
from geopy import geocoders, exc # library to map country names-codes-geocoordinates. Requires registration
from geopy.extra.rate_limiter import RateLimiter


# # Initialize configuration

# In[2]:


# Pandas 
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Web scraping
url = "https://www.worldometers.info/coronavirus/"
na_value = "NaN"
dataset_filename = "covid-19_global_spread.csv"


# # Functions

# In[3]:


def run_web_scraper(url):
        
    # Send request
    wurl = requests.get(url).text
    soup = BeautifulSoup(wurl,'lxml')

    # Get rows
    rows = soup.find('table').find('tbody').find_all('tr')  

    # Statistics
    rows_number = len(rows)
    columns_number = len(rows[0].find_all('td'))
    print("  -There are",rows_number,"rows in the table")
    print("  -There are",columns_number,"columns in the table")

    # Get array from rows
    data = [[item.text.strip() for item in row.find_all('td')] for row in rows]

    # Transform to pandas dataframe
    header = ['Country','Total cases','New cases','Total deaths','New deaths','Total recovered',
              'Active cases','Critical cases','Cases/1M pop']
    data_pd = pd.DataFrame(data, columns=header)
    
    # Return
    return data_pd


# In[4]:


def get_geocoordinates(data,column_name,lon_column_name, lat_column_name):
    
    # Initialize geolocator
    geolocator = geocoders.Nominatim(user_agent="xxx",timeout=None)
    
    # Generate longitude and latitude variables
    longitude = [geolocator.geocode(item).longitude for item in data[column_name]]
    latitude = [geolocator.geocode(item).latitude for item in data[column_name]]
    
    # Define in dataset
    data[lon_column_name] = longitude
    data[lat_column_name] = latitude
    
    # Return
    return data


# In[5]:


def data_preparation(data):
    
    # Remove ','
    data=data.replace({',': ''}, regex=True)
    
    # Remove first char
    data['New cases'] = (data['New cases'].str[1:])
    data['New deaths'] = (data['New deaths'].str[1:])
    
    # Set missing values as NaN
    data=data.replace('','NaN')
    
    # Fix variable type
    data[['Total cases','New cases','Total deaths','New deaths','Total recovered',
          'Active cases','Critical cases','Cases/1M pop']] = data[['Total cases','New cases','Total deaths','New deaths',
                                                                   'Total recovered','Active cases','Critical cases',
                                                                   'Cases/1M pop']].astype(float)
    
    # Get geocoordinates from country name
    data = get_geocoordinates(data,"Country","Lon","Lat")

    # Return    
    return data


# In[6]:


def data_visualization(data):
    
    # Generate world chart
    fig = px.scatter_geo(clean_data, lon = clean_data['Lon'], lat = clean_data['Lat'], color="Country",
                         hover_name="Country", size="Total cases", projection="equirectangular")
    
    # Print world chart
    fig.show()
    
    # Save world chart
    fig.write_image('covid-19_global_spread_chart.png')   
    
    # Generate bar chart
    fig = data.head(10).plot(x="Country", y=["Total cases","Active cases","Total recovered", "Total deaths"],
                             kind="bar", figsize=(20,10)).get_figure()
    
    plt.show()
    
    # Print bar chart
    fig.savefig('covid-19_top_10_countries.png')    


# # Main

# In[7]:


# Run web scraper
print('\n1. Web scraping')
raw_data = run_web_scraper(url)

# Prepare data
print('\n2. Data preparation')
clean_data = data_preparation(raw_data)

# Export to csv
print('\n3. Export to csv')
clean_data.to_csv(dataset_filename, index=False, na_rep=na_value)

# Data visualization
print('\n4. Visualization')
data_visualization(clean_data)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




