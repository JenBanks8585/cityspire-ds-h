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
from app.helper import *


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
async def get_walk_score(city:str, state: str):
    """
    Parameters: 
        city: string
        state: 2-letter state Abbreviation
    Returns: dict
        Returns walkscore, description, transit score and bike score
    """

    response = just_walk_score(city, state)

    return response



@router.get('/pollution')
async def get_pollution(city:str, state: str):
    """ Input: City, 2 letter abbreviation for state
    Returns a list containing WalkScore, BusScore, and BikeScore in that order
    """    
    response = pollution(city)
    
    return response