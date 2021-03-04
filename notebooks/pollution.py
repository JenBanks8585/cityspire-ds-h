
# Define variable and set server credentials 

import chart_studio
username ='jennifer.banks8585'
api_key= 'OTqsX5g5OFYR7MdF6mBI'
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

#imports
import chart_studio.plotly as py
import chart_studio.tools as tls
import plotly.graph_objects as go
import pandas as pd

# Data
air = pd.read_csv('https://raw.githubusercontent.com/JenBanks8585/Randomdata/main/data/Pollution/daily_aqi_by_county_2020.csv')
air = air[["State Name", "county Name", "Date", "AQI", "Category", "Defining Parameter"]]

# Transform to long format
air_melt = pd.melt(air, id_vars=["State Name", "county Name", "Category", "Date", "Defining Parameter"])
air_melt = air_melt.drop(columns = "variable", axis =0)
air_melt['Date'] = pd.to_datetime(air_melt['Date'])
air_melt['Month']=  pd.DatetimeIndex(air_melt['Date']).month

# Group values
air_melt_grouped = air_melt.groupby(["Date","county Name","State Name","Month", "Defining Parameter", "Category"]).mean()
air_melt_grouped['value']= air_melt_grouped['value'].astype(int)
air_melt_grouped = air_melt_grouped.reset_index()

# Visualization function

def plot_pollution(county, state):
  aqi = air_melt_grouped[(air_melt_grouped['county Name']==county) & (air_melt_grouped['State Name']==state)]

  fig = go.Figure()
  fig.add_trace(go.Scatter(name="Observed", 
                             x=list(aqi['Month']), 
                             y=list(aqi['value']),                          
                                    
        fill=None,
        mode='markers',
        line_color='red'))
    
  fig.update_layout({
        'autosize':False,
        'plot_bgcolor':'rgba(2,0,0,5)',
        'paper_bgcolor':'rgba(2,0,0,5)',
        'font_color':"white",
        'title': f'Region name: {county}, {state}',
        'yaxis_title': 'Air Quality Index',
        'xaxis_title': 'Month in 2020'
        })
    
  fig.update_yaxes(automargin = True, gridcolor = "gray")
  fig.update_xaxes(automargin = True, gridcolor = "gray")
   
  fig.show()

  return py.plot(fig, filename="pollution", auto_open = True)
