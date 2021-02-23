"""Database functions"""

import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
import sqlalchemy
import json
from pydantic import BaseModel
import pandas as pd
from app.helper import get_city_id

router = APIRouter()


async def get_db() -> sqlalchemy.engine.base.Connection:
    """Get a SQLAlchemy database connection.
    
    Uses this environment variable if it exists:  
    DATABASE_URL=dialect://user:password@host/dbname

    Otherwise uses a SQLite database for initial local development.
    """
    load_dotenv()
    database_url = os.getenv('PRODUCTION_DATABASE_URL', default='sqlite:///temporary.db')
    engine = sqlalchemy.create_engine(database_url)
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()


@router.get('/info')
async def get_url(connection=Depends(get_db)):
    """Verify we can connect to the database, 
    and return the database URL in this format:

    dialect://user:password@host/dbname

    The password will be hidden with ***
    """
    url_without_password = repr(connection.engine.url)
    return {'database_url': url_without_password}


@router.get('/city_list')
async def city_list():
    '''
    Returns a list of all cities that are in the database
    returns city_name and state_name
    '''
    load_dotenv()
    database_url = os.getenv('PRODUCTION_DATABASE_URL')
    query = '''SELECT Cities.city_name, STATES.state_name
                FROM CITIES
                LEFT JOIN STATES ON CITIES.state_id=STATES.state_id
            '''
    engine = sqlalchemy.create_engine(database_url)
    cities = engine.execute(query)
    city_list = []
    for each in cities:
        city_list.append({'city_name':f'{each[0].strip()}', 'state_name':f'{each[1].strip()}'})
    to_return = json.dumps(city_list)
    return to_return

@router.get('/state_list')
async def state_list():
    '''
    Returns a list of all states that are in the database
    returns state_name and state_abbreviation
    '''
    load_dotenv()
    database_url = os.getenv('PRODUCTION_DATABASE_URL')
    query = '''SELECT state_name, state_abbreviation
                FROM STATES
            '''
    engine = sqlalchemy.create_engine(database_url)
    states = engine.execute(query)
    state_list = []
    for each in states:
        state_list.append(({'state_name':f'{each[0].strip()}', 'state_abbreviation':f'{each[1].strip()}'}))
    to_return = json.dumps(state_list)
    return to_return

class LocationQuery(BaseModel):
    city_name: str
    state_name: str

@router.post('/location')
async def location(locationquery: LocationQuery):
    city_name = locationquery.city_name
    state_name = locationquery.state_name
    load_dotenv()
    database_url = os.getenv('PRODUCTION_DATABASE_URL')
    engine = sqlalchemy.create_engine(database_url)
    if city_name == '' and state_name == '':
        query = f'''
                SELECT Cities.city_name, STATES.state_name, Cities.latitude, Cities.longitude
                FROM CITIES
                LEFT JOIN STATES ON CITIES.state_id=STATES.state_id
                '''
    elif city_name == '':
        query = f'''
                SELECT Cities.city_name, STATES.state_name, Cities.latitude, Cities.longitude
                FROM CITIES
                LEFT JOIN STATES ON CITIES.state_id=STATES.state_id
                Where STATES.state_name = \'{state_name}\'
                '''
    elif state_name == '':
        query = f'''
                SELECT Cities.city_name, STATES.state_name, Cities.latitude, Cities.longitude
                FROM CITIES
                LEFT JOIN STATES ON CITIES.state_id=STATES.state_id
                Where cities.city_name = \'{city_name}\'
                '''
    else:
        query = f'''
                 SELECT Cities.city_name, STATES.state_name, Cities.latitude, Cities.longitude
                FROM CITIES
                LEFT JOIN STATES ON CITIES.state_id=STATES.state_id
                Where cities.city_name = \'{city_name}\' and states.state_name = \'{state_name}\'
                '''
    query_result = engine.execute(query)
    location_list = []
    for each in query_result:
        location_list.append({'city_name':f'{each[0].strip()}',
        'state_name': f'{each[1].strip()}',
        'latitude': f'{each[2]}',
        'longitude': f'{each[3]}'})
    to_return = json.dumps(location_list)
    return to_return




class CrimeQuery(BaseModel):
    city_name: str
    state_abbreviation: str

@router.post('/crime_data')
async def crime_data(crimequery: CrimeQuery):
    city_name = crimequery.city_name
    state_abbreviation = crimequery.state_abbreviation
    city_id = get_city_id(city_name, state_abbreviation)

    load_dotenv()
    DATABASE_URL = os.getenv('PRODUCTION_DATABASE_URL')
    
    crime_features = ['violent_crime', 'murder_and_nonnegligent_homicide',
                'rape', 'robbery', 'aggravated_assault', 'property_crime', 'burglary',
                'larceny_theft', 'motor_vehicle_theft', 'arson', 'total']

    # raw data
    query = f'''
                 SELECT year, RTRIM(type) as type, value
                FROM city_crime_data_raw
                WHERE city_id = \'{city_id}\'
                '''
    raw = pd.read_sql(query, DATABASE_URL)
    
    raw_dict = {'year':raw['year'].max()}
    for each in crime_features:
        raw_dict[each] = raw[(raw['year'] == raw['year'].max()) & (raw['type'] == f'{each}')]['value']
        
        if len(raw_dict[each]) == 1:
            raw_dict[each] = raw_dict[each].iloc[0]
        else:
            raw_dict[each] = 'n/a'
    for key, value in raw_dict.items():
        raw_dict[key] = int(raw_dict[key])

    # per_capita data
    query = f'''
                 SELECT year, RTRIM(type) as type, value
                FROM city_crime_data_per_capita
                WHERE city_id = \'{city_id}\'
                '''
    per_capita = pd.read_sql(query, DATABASE_URL)

    per_capita_dict = {'year':per_capita['year'].max()}
    for each in crime_features:
        per_capita_dict[each] = per_capita[(per_capita['year'] == per_capita['year'].max()) & (per_capita['type'] == f'{each}')]['value']
        
        if len(per_capita_dict[each]) == 1:
            per_capita_dict[each] = per_capita_dict[each].iloc[0]
        else:
            per_capita_dict[each] = 'n/a'
    for key, value in per_capita_dict.items():
        per_capita_dict[key] = float(per_capita_dict[key])

    to_return = json.dumps({'raw': raw_dict, 'per_capita': per_capita_dict})
    return to_return

class PopulationQuery(BaseModel):
    city_name: str
    state_abbreviation: str

@router.post('/population_data')
async def population_data(populationquery: PopulationQuery):
    try:
        city_name = populationquery.city_name
        state_abbreviation = populationquery.state_abbreviation
        city_id = get_city_id(city_name, state_abbreviation)

        load_dotenv()
        DATABASE_URL = os.getenv('PRODUCTION_DATABASE_URL')

        engine = sqlalchemy.create_engine(DATABASE_URL)
        query = f'''
                SELECT population
                FROM city_population
                WHERE city_id = \'{city_id}\' and year = (SELECT max(year) From city_population WHERE city_id = \'{city_id}\')
                '''
        query_result = engine.execute(query)
        my_return = [each[0] for each in query_result]
        return json.dumps({'population': my_return[0]})
    except:
        return json.dumps({'population': 'n/a'})