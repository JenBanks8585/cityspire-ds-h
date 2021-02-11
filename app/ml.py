import os

import pandas as pd 
from fastapi import APIRouter, Depends
from pydantic import BaseModel, SecretStr
import sqlalchemy
import json

from dotenv import load_dotenv


router = APIRouter()
  

class RentForecast(BaseModel):
    city_name: str   
    state_name: str

@router.post('/rentforecast_cityname')
async def forecast_list(rentforecast:RentForecast):
    """
    Parameters: 
        city_name: str
        
    Returns: dict
        Rent forecast in the next 5 months with low and high range
    """
    city_name = rentforecast.city_name    
    load_dotenv()
    database_url = os.getenv('PRODUCTION_DATABASE_URL')
    engine = sqlalchemy.create_engine(database_url)

    query = '''SELECT RTRIM(CITIES.city_name) as city_name, RENTAL_FORECAST.rental_forecast
    FROM CITIES
    INNER JOIN RENTAL_FORECAST 
    ON CITIES.city_id=RENTAL_FORECAST.city_id  
    '''
    query_result = engine.execute(query)
    forecasts = query_result.fetchall()

    for i in range(len(forecasts)):
        if forecasts[i][0]== city_name:

            return forecasts[i][1]
    

@router.get('/rent_forecast_zip')
async def give_forecast(zip: str = '01852'):

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