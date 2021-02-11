"""Realty Info"""

import os
import requests

import json
import sqlalchemy
import pandas as pd 
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from pydantic import BaseModel, SecretStr
from walkscore import WalkScoreAPI

from app import config
from app.pollution import *


load_dotenv()

router = APIRouter()


headers={'x-rapidapi-key': os.getenv('api_key'),
            'x-rapidapi-host': os.getenv('host')}



@router.get('/streamlined_rent_list')
async def streamlined_rent_list(api_key=config.settings.api_key, 
             city: str="New York City", 
             state: str="NY", 
             prop_type: str="condo", 
             limit: int=4):

    """
    Parameters:
        api_key
        city: str 
        state: str Two-letter abbreviation
        prop_type: str ('condo', 'single_family', 'multi_family')
        limit: int number of results to populate

    Returns: dict
        Chosen information of the requested parameters such 
        as addresses, state, ciy, lat, lon, photos, walk score, pollution info
    """
    
    url=os.getenv('url_list_for_rent')
    querystring={"city": city,
                 "state_code": state,
                 "limit": limit,
                 "offset": "0",                 
                 "sort":"relevance",
                 "prop_type": prop_type}

    response_for_rent=requests.request("GET", url, params=querystring, headers=headers,)
    response = response_for_rent.json()['properties']
    pollution_res = pollution(city)


    rental_list=[]
    for i in range(limit):
      line=response[i]['address']['line']
      city=response[i]['address']['city']
      state=response[i]['address']['state']
      lat=response[i]['address']['lat']
      lon=response[i]['address']['lon']
      photos=response[i]['photos']
      element={ 'lat': lat, 
                'lon': lon, 
                'city':city, 
                'state':state, 
                'photos': photos,
                'pollution': pollution_res}
                                 

      rental_list.append(element)

    return rental_list


@router.get('/for_rent_list')
async def for_rent_list(api_key=config.settings.api_key, 
             city: str="New York City", 
             state: str="NY", 
             prop_type: str="condo", 
             limit: int=4):
    """
    Parameters:
        api_key
        city: str 
        state: str
        prop_type: str ('condo', 'single_family', 'multi_family')
        limit: int number of results to populate

    Returns: dict
        Expanded information about the city 
    """

    url=os.getenv('url_list_for_rent')
    querystring={"city": city,
                 "state_code": state,
                 "limit": limit,
                 "offset": "0",                 
                 "sort":"relevance",
                 "prop_type": prop_type}

    response_for_rent=requests.request("GET", url, 
                        params=querystring, 
                        headers=headers)

    return response_for_rent.json()['properties']


@router.get('/for_rent_list/{property_id}')
async def property_detail(property_id: str="O3599084026"):
    """
    Parameters: 
        property_id
    Returns: dict
        detailed information about the property
    """

    url=os.getenv('url_property_detail')
    querystring={"property_id":property_id}
    
    response_prop_detail=requests.request("GET", url, 
                            headers=headers, 
                            params=querystring)

    return response_prop_detail.json()['properties']


@router.get('/for_sale_list')
async def for_sale_list(api_key=config.settings.api_key, 
             city="New York City", 
             state="NY",             
             limit=4):
    """
    Parameters: 
        city: str
        state: str
        limit: int number of results to populate
    Returns: dict
        detailed information about the property
    """

    url=os.getenv('url_list_for_sale')
    querystring={"city": city ,
                    "limit": limit,
                    "offset":"0",
                    "state_code": state,
                    "sort":"relevance"}

    response_for_sale=requests.request("GET", url, headers=headers, params=querystring)
    return response_for_sale.json()['properties']


@router.get('/walk_score')
async def get_walk_score(address: str = "7 New Port Beach, Louisiana",
    lat: float = 39.5984,
    lon: float = -74.2151):

    """
    Parameters: 
        address: str
        lat: float
        lon: float number of results to populate
    Returns: dict
        Returns walkscore, description, transit score and bike score
    """

    walk_api = WalkScoreAPI(api_key= os.getenv('walk_api'))

    result = walk_api.get_score(longitude = lon, 
            latitude = lat,
            address = address)
    
    message = what_message(result.walk_score)

    response = {"walk_score": result.walk_score, 
                "walk_message":message, 
                "transit_score": result.transit_score, 
                "bike_score": result.bike_score}
    return response


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


def just_walk_score(address: str = "7 New Port Beach, Louisiana",
    lat: float = 39.5984,
    lon: float = -74.2151
    ):

    walk_api = WalkScoreAPI(api_key= os.getenv('walk_api'))

    result = walk_api.get_score(longitude = lon, 
            latitude = lat,
            address = address)
    
    message = what_message(result.walk_score)

    response = {"walk_score": result.walk_score, 
                "walk_message":message, 
                "transit_score": result.transit_score, 
                "bike_score": result.bike_score}
    return response


url =  os.getenv('zip_forecast')

rental_forecast_zip = pd.read_csv(url, index_col=[0])
rental_forecast_zip['zip'] = rental_forecast_zip['zip'].apply(lambda x: str(x).zfill(5))


@router.get('/rent_forecast_zip')
async def give_forecast(zip: str = '01852'):

    """
    Parameters: 
        zip: str        
    Returns: dict
        Rent forecast in the next 5 months with low and high range
    """

    if zip in list(rental_forecast_zip['zip']):
        forecast = rental_forecast_zip.loc[rental_forecast_zip['zip']==zip, 'forecast'].item()
        return forecast 
    return "No forecast for this location"
