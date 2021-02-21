"""Data visualization functions"""

import os
import requests

import json
import sqlalchemy
import pandas as pd 
from dotenv import load_dotenv
import plotly.graph_objects as go
from walkscore import WalkScoreAPI
from fastapi import APIRouter, Depends
from pydantic import BaseModel, SecretStr
from fastapi import APIRouter

from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

AQI= ['0-50', '51-100', '101-150', '151-200', '201-300', '300-500']
Level = ['Good', 'Moderate', 'Unhealthy for Sensitive Group', 'Unhealthy', 'Very Unhealthy', 'Hazardous']
Health_Implications =['Air quality is considered satisfactory, and air pollution poses little or no risk',
                      'Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution.',
                      'Members of sensitive groups may experience health effects. The general public is not likely to be affected.',
                      'Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects',
                      'Health warnings of emergency conditions. The entire population is more likely to be affected',
                      'Health alert: everyone may experience more serious health effects'
                      ]
Cautionary_Statement_PM2_5 = ['None',
                               'Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion.',
                               'Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion.',
                               'Active children and adults, and people with respiratory disease, such as asthma, should avoid prolonged outdoor exertion; everyone else, especially children, should limit prolonged outdoor exertion',
                               'Active children and adults, and people with respiratory disease, such as asthma, should avoid all outdoor exertion; everyone else, especially children, should limit outdoor exertion.',
                               'Everyone should avoid all outdoor exertion']


d_lst = []
for i in range(len(AQI)):
  a = {'Health_Implications':Health_Implications[i],'Cautinary_statement_PM2.5':Cautionary_Statement_PM2_5[i]}
  d_lst.append(a)


def pollution_range(aqi_index: int):
  if 0 <= aqi_index and aqi_index <= 51:
    return d_lst[0]
  elif 51<=aqi_index and aqi_index <=100:
    return d_lst[1]
  elif 101<=aqi_index and aqi_index <=150:
    return d_lst[2]
  elif 151<=aqi_index and aqi_index <=200:
    return d_lst[3]
  elif 201<=aqi_index and aqi_index  <=300:
    return d_lst[4]
  else:
    return d_lst[5]


def pollution(city:str):
    """ Input: City, 2 letter abbreviation for state
    Returns a list containing WalkScore, BusScore, and BikeScore in that order
    """    
    token = os.getenv('token')
    r= requests.get(f"https://api.waqi.info/feed/{city}/?token={token}")
    result = r.json()['data']

    if result == 'Unknown station' or result =='-':
      return 'No data for this city'
    
    else: 
      if result['aqi'] == '-':
        return "No data for this city"

      aqi = result['aqi']
      description= pollution_range(aqi_index= aqi)
      response = {f'AQI_index: {aqi}, description :{description}'} 
    
    return response


def get_aqi_rate(city:str, state:str):
  """
  Parameters: 
  city: Name of city in US
  state: Two-letter abbreviation of state
  """
  openweather_key =os.getenv("openweathermap_api")
  
  requ = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},USA&limit={1}&appid={openweather_key}")
  lat= requ.json()[0]['lat']
  lon= requ.json()[0]['lon']

  req = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={openweather_key}")
  aqi = req.json()['list'][0]['main']['aqi']
  aqi_dict= {1:90, 2:70, 3:50, 4:30, 5:10}
  aqi_value = aqi_dict[aqi]

  return aqi_value



def what_message(score):
    if 90 <= score <= 100:
        return "daily errands do not require a car"
    elif 70 <= score <= 89:
        return "most errands can be accomplished on foot"
    elif 50 <= score <= 69:
        return "some errands can be accomplished on foot"
    elif 25 <= score <= 49:
        return "most errands require a car"
    else:
        return " almost all errands require a car"


def just_walk_score(city:str, state: str):
    """
    Parameters: 
        city: string
        state: 2-letter state Abbreviation
    Returns: dict
        Returns walkscore, description, transit score and bike score
    """

    openweather_key=os.getenv("openweathermap_api")
    requ = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},USA&limit={1}&appid={openweather_key}")
    lat= requ.json()[0]['lat']
    lon= requ.json()[0]['lon']

    walk_api = WalkScoreAPI(api_key= os.getenv('walk_api'))
    result = walk_api.get_score(longitude = lon, 
            latitude = lat)
    
    message = what_message(result.walk_score)

    response = {"walk_score": result.walk_score, 
                "walk_message":message, 
                "transit_score": result.transit_score, 
                "bike_score": result.bike_score}
    return response


def load_data_rent_visual():
  """
  Helper function that loads data for processing for rent forecast visualization
  """
  url_forecast=os.getenv("url_forecast")
  url_training=os.getenv("url_training")
  # Forecast data
  df = pd.read_csv(url_forecast, index_col = [0])
  df.columns = ['zip', 'city', 'state', 'level', '2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', '2021-05-01']
  # Convert to long format
  df_melt = pd.melt(df, id_vars=['zip', 'city', 'state', 'level'])
  # Rename columns
  df_melt.columns = ['zip', 'city', 'state', 'level', 'month','rent_forecast']
  # Cast date to datetime object
  df_melt['month']= pd.to_datetime(df_melt['month'], infer_datetime_format=True)
  # Training data
  df_orig = pd.read_csv(url_training, parse_dates= True)
  df_orig = df_orig.drop(columns =['SizeRank'], axis = 0)
  # labels
  df_1= df_orig.iloc[:,1:3]
  # Grabbing data from 2018 onwards
  df_2= df_orig.iloc[:,60:]
  # Concatenate
  df_me = pd.concat([df_1, df_2], axis = 1)
  # Transform to long format
  df_mew = pd.melt(df_me, id_vars=['RegionName', 'MsaName'])
  # Grab columns
  df_mew.columns =['zip', 'cityname', 'date', 'rent_forecast']
  # Cast date to datetime object
  df_mew['date']= pd.to_datetime(df_mew['date'])
  return df_melt, df_me, df_mew

def get_city_id(city_name, state_abbreviation):
  load_dotenv()
  database_url = os.getenv('PRODUCTION_DATABASE_URL')
  engine = sqlalchemy.create_engine(database_url)
  city_name = city_name.title()
  state_abbreviation = state_abbreviation.upper()
  query = f'''
    SELECT Cities.city_id
    FROM CITIES
    LEFT JOIN STATES ON CITIES.state_id=STATES.state_id
    Where cities.city_name = \'{city_name}\' and states.state_abbreviation = \'{state_abbreviation}\'
    '''
  query_result = engine.execute(query)
  my_return = [each[0] for each in query_result]
  return my_return[0]


def get_community_rate(state:str):
  """
  Parameter:
    state: Two-letter abbreviation of the state
  Returns:
    Overall rating that includes affordability, education, health, safety
  """
  url_best_state_to_live=os.getenv("url_best_state_to_live")
  url_state_abbrev=os.getenv("url_state_abbrev")

  best_state_to_live =pd.read_csv(url_best_state_to_live)
  state_abbrev = pd.read_csv(url_state_abbrev)

  best_state_with_abbrev = pd.merge(best_state_to_live,state_abbrev, on = 'State')
  states = list(best_state_with_abbrev['Abbreviation'])
  if state in states:
    score = best_state_with_abbrev.loc[best_state_with_abbrev['Abbreviation']==state, 'Total Score'].item()
    return score
  else:
    return {'message': "No data for this location"}


def housing_affordability_rate(state):
  """
  Parameter:
    state: Two-letter abbreviation of the state
  Returns:
    Housing affordability rate by state
  """
  url_housing_affordability=os.getenv("url_housing_affordability")
  housing_affordability = pd.read_csv(url_housing_affordability)
  housing_affordability['State'] = housing_affordability['Metro Area*'].apply(lambda x: x.split(",")[-1].strip())
  rate_by_state = housing_affordability.loc[housing_affordability['State']==state, "2019 Q3"].max()
  highest= housing_affordability["2019 Q3"].max()
  score = 100*(1.5-(rate_by_state/highest))
  return score
