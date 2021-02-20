import os

import pandas as pd 
from fastapi import APIRouter, Depends
from pydantic import BaseModel, SecretStr
import sqlalchemy
import json

from dotenv import load_dotenv


load_dotenv()
database_url = os.getenv('PRODUCTION_DATABASE_URL')
engine = sqlalchemy.create_engine(database_url)
query = '''SELECT RTRIM(CITIES.city_name) as city_name,                
                CITY_POPULATION.POPULATION,
                CITY_POPULATION.year,
                STATES.state_abbreviation
            FROM CITIES
            INNER JOIN CITY_POPULATION
                ON CITIES.city_id=CITY_POPULATION.city_id  
            INNER JOIN STATES
                ON CITIES.state_id = STATES.state_id

            '''

df =pd.read_sql(query, database_url)
df.to_csv("population_for_visual.csv")