import os

import pandas as pd 
from fastapi import APIRouter, Depends
from pydantic import BaseModel, SecretStr
import sqlalchemy
import json
from app.helper import get_city_id, just_walk_score, get_aqi_rate, overall_rate

from dotenv import load_dotenv


router = APIRouter()
  

class RentForecast(BaseModel):
    city_name: str   
    state_abbrev: str

@router.post('/rentforecast_cityname')
async def give_forecast_by_cityname(rentforecast:RentForecast):
    """
    Parameters: 
        city_name: str  Capital first letter    
        state_abbrev: str Two-letter capitalized abbrevation of state  
    Returns: dict
        Rent forecast in the next 5 months with low and high range
    """

    city_name = rentforecast.city_name
    state_abbrev = rentforecast.state_abbrev
    
    load_dotenv()
    database_url = os.getenv('PRODUCTION_DATABASE_URL')
    engine = sqlalchemy.create_engine(database_url)
    query = '''SELECT RTRIM(CITIES.city_name) as city_name, 
                      RENTAL_FORECAST.rental_forecast,
                      RTRIM(STATES.state_abbreviation) as state_name    
                FROM CITIES
                INNER JOIN RENTAL_FORECAST 
                    ON CITIES.city_id=RENTAL_FORECAST.city_id  
                INNER JOIN STATES
                    ON CITIES.state_id = STATES.state_id
                '''
    query_result = engine.execute(query)
    forecasts = query_result.fetchall()
    for i in range(len(forecasts)):
        if forecasts[i][0]== city_name and forecasts[i][2]==state_abbrev:
            return forecasts[i][1]

    return 'Data for this location is not available'
    

@router.get('/rent_forecast_zip')
async def give_forecast_by_zip(zip: str = '01852'):

    """
    Parameters: 
        zip: str        
    Returns: dict
        Rent forecast in the next 5 months with low and high range
    """
    url =  os.getenv('zip_forecast')
    rental_forecast_zip = pd.read_csv(url, index_col=[0])
    rental_forecast_zip['zip'] = rental_forecast_zip['zip'].apply(lambda x: str(x).zfill(5))
    
    if zip in list(rental_forecast_zip['zip']):
        forecast = rental_forecast_zip.loc[rental_forecast_zip['zip']==zip, 'forecast'].item()
        return forecast 
    return "No forecast for this location"

class LivabilityQuery(BaseModel):
    city_name: str
    state_abbreviation: str

@router.post('/livability')
async def livability(livabilityquery: LivabilityQuery):
    city_name = livabilityquery.city_name
    state_abbreviation = livabilityquery.state_abbreviation
    city_id = get_city_id(city_name, state_abbreviation)
    livability_dict = {}

    # population
    livability_dict['population'] = 50

    # crime
    livability_dict['crime'] = 50


    # walk score
    livability_dict['walk_score']=just_walk_score(city_name, state_abbreviation)['walk_score'] 

    
    # pollution
    livability_dict['pollution'] = get_aqi_rate(city_name, state_abbreviation)


    # computing affordability, education, safety
    livability_dict['overall'] = overall_rate(state_abbreviation)
    

    # computing livability
    sum = 0
    len = 0
    for key, value in livability_dict.items():
        sum += value
        len += 1

    livability = sum / len


    to_return = {'livability': livability}
    return json.dumps(to_return)