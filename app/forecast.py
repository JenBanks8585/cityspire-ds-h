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

@router.post('/rentforecast_cityname')
async def forecast_list(rentforecast:RentForecast):
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
    