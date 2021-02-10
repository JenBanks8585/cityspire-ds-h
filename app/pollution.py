"""Data visualization functions"""

import os
import requests

import json
import sqlalchemy
import pandas as pd 
from dotenv import load_dotenv
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


@router.get('/pollution')
async def get_pollution(city:str):
    """ Input: City, 2 letter abbreviation for state
    Returns a list containing WalkScore, BusScore, and BikeScore in that order
    """    
    response = pollution(city)
    
    return response