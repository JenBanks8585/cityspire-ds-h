"""Database functions"""

import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
import sqlalchemy
import json
from pydantic import BaseModel

router = APIRouter()


async def get_db() -> sqlalchemy.engine.base.Connection:
    """Get a SQLAlchemy database connection.
    
    Uses this environment variable if it exists:  
    DATABASE_URL=dialect://user:password@host/dbname

    Otherwise uses a SQLite database for initial local development.
    """
    load_dotenv()
    database_url = os.getenv('DEVELOPMENT_DATABASE_URL', default='sqlite:///temporary.db')
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
    database_url = os.getenv('DEVELOPMENT_DATABASE_URL')
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
    database_url = os.getenv('DEVELOPMENT_DATABASE_URL')
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
    database_url = os.getenv('DEVELOPMENT_DATABASE_URL')
    engine = sqlalchemy.create_engine(database_url)
    if city_name == '':
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

