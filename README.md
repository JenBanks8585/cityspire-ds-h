<p align="center">
  <img src="https://github.com/FabiolaSaga/GOL/blob/main/CitySpireLogo-Dark.png">
</p>

## Link

* [DS API](https://h-ds2.cityspire.dev/)

## Framework

* FastAPI, deployed on AWS Elastic Beanstalk

## Endpoints

* ## Database

 `/city_list` : Returns a list of all cities that are in the database returns city_name and state_name

 `/state_list`: Returns a list of all states that are in the database returns state_name and state_abbreviation

 `/location`: Returns a list of json objects that match the search criteria. If city_name or state_name are left blank then it is likely there will be more than one result.

 ```
 "[{\"city_name\": \"Atlanta\", \"state_name\": \"Georgia\", \"latitude\": \"33.762909\", \"longitude\": \"-84.422675\"}]"
 ```

 `/crime_data`: Returns a json format of different types of crimes and corresponding years and counts

 ```
 "{\"raw\": {\"year\": 2018, \"violent_crime\": 3814, \"murder_and_nonnegligent_homicide\": 88, \"rape\": 245, \"robbery\": 1099, \"aggravated_assault\": 2382, \"property_crime\": 23091, \"burglary\": 3082, \"larceny_theft\": 16701, \"motor_vehicle_theft\": 3308, \"arson\": 90, \"total\": 53900}, \"per_capita\": {\"year\": 2018.0, \"violent_crime\": 0.0076558213, \"murder_and_nonnegligent_homicide\": 0.00017664192, \"rape\": 0.00049178716, \"robbery\": 0.0022060166, \"aggravated_assault\": 0.0047813756, \"property_crime\": 0.04635044, \"burglary\": 0.0061864816, \"larceny_theft\": 0.033523824, \"motor_vehicle_theft\": 0.00664013, \"arson\": 0.00018065651, \"total\": 0.108193174}}"
 ```

 `/population_data`: Returns the population count based on city and state

 ```
 "{\"population\": 506811}"
 ```

 ![Database Schema](https://github.com/JenBanks8585/Randomdata/blob/main/visuals/b.PNG)

 * ## Machine Learning

 `/rentforecast_cityname`: Returns a low and high forecasts for the next 5 months per city given city_name

 ```[
  {
    "in_1_month": {
      "low": 1256,
      "high": 1443
    }
  },
  {
    "in_2_months": {
      "low": 1242,
      "high": 1464
    }
  },
  {
    "in_3_months": {
      "low": 1238,
      "high": 1472
    }
  },
  {
    "in_4_months": {
      "low": 1236,
      "high": 1475
    }
  },
  {
    "in_5_months": {
      "low": 1236,
      "high": 1478
    }
  }
]
```

 `/rent_forecast_zip`: Returns a low and high forecasts for the next 5 months per city given the zip code

 `/livability`: Returns the livability score by city

 ```
 "{\"livability\": 67.03685823754789}"
 ```

 * ## External Resources

 `/streamlined_rent_list`: Returns dict of chosen information of the requested parameters such as addresses, state, ciy, lat, lon, photos, walk score, pollution info

 ```
  {
    "lat": 40.743489,
    "lon": -74.006386,
    "city": "New York",
    "state": "New York",
    "photos": [
      {
        "href": "https://ar.rdcpix.com/c1d9edff7979b27e51c532149940f0adc-f4151003418o.jpg"
      },
      {
        "href": "https://ar.rdcpix.com/c1d9edff7979b27e51c532149940f0adc-f3646394273o.jpg"
      },
      {
        "href": "https://ar.rdcpix.com/c1d9edff7979b27e51c532149940f0adc-f1517791643o.jpg"
      },
      {
        "href": "https://ar.rdcpix.com/c1d9edff7979b27e51c532149940f0adc-f2486854284o.jpg"
      }
    ],
    "pollution": [
      "AQI_index: 40, description :{'Health_Implications': 'Air quality is considered satisfactory, and air pollution poses little or no risk', 'Cautinary_statement_PM2.5': 'None'}"
    ]
  }
  ```

 `/for_rent_list`: Returns expanded set of information about a locations rental availability

 `/for_rent_list{property_id}`: Returns information about a specific property

 `/for_sale_list`: Returns list of properties for sale and their corresponding information

 `/walk_score`: Returns the walkscore and its corresponding description, bike score and transit score.

 ```
 {
  "walk_score": 67,
  "walk_message": "some errands can be accomplished on foot",
  "transit_score": null,
  "bike_score": 45
}
```

`/pollution`: Returns Air Quality Index(AQI) and corresponding description

```
[
  "AQI_index: 28, description :{'Health_Implications': 'Air quality is considered satisfactory, and air pollution poses little or no risk', 'Cautinary_statement_PM2.5': 'None'}"
]
```

* ## Visualization

 `/rentforecast_visualize`: Returns a json format of visualization properties
 
 ![Boston](https://github.com/JenBanks8585/Randomdata/blob/main/visuals/a.PNG)


### Project Lead
|                                                      [Bobby Hall Jr](https://github.com/bobbyhalljr)                                                      |
| :-----------------------------------------------------------------------------------------------------------------------------------------: |
| [<img src="https://avatars.githubusercontent.com/u/29504858?s=400&v=4" width = "150" />](https://github.com/bobbyhalljr) |
|                                [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/bobbyhalljr)                                |
|                [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/bobbyhalljr/)                | 

### iOS Contributors

|                                                      [Jarren Campos](https://github.com/jarrencampos)                                                      |                                                       [Fabiola Saldivar](https://github.com/FabiolaSaga)                                                     
| :-----------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------: |
| [<img src="https://avatars.githubusercontent.com/u/57583547?s=400&u=bed4c66a1e346bbfb6a09616b2c716d3833a6e55&v=4" width = "150" />](https://github.com/jarrencampos) | [<img src="https://avatars.githubusercontent.com/u/35746731?s=400&u=5f68d9c3808b46b4ac25f0abe01e68bf360e91f6&v=4" width = "150" />](https://github.com/FabiolaSaga) | 
|                                [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/jarrencampos)                                |                            [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/FabiolaSaga)                             |                            
|                [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/jarrencampos/)                |                 [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/fabiolasaga/)                 |           


### [Data Science Contributors](https://github.com/Lambda-School-Labs/cityspire-ds-h)
|                                                      [Jennifer Banks](https://github.com/JenBanks8585)                                                      |                                                       [Zachary Hamilton](https://github.com/zachary-hamilton)                                                     
| :-----------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------: |
| [<img src="https://avatars.githubusercontent.com/u/59672512?s=400&u=d86b9369f4a61d757cde9181dc2561a4393be225&v=4" width = "150" />](https://github.com/JenBanks8585) | [<img src="https://avatars.githubusercontent.com/u/57552986?s=400&u=929fc46fb460a9d60e8d5f1172cf2fa76e876953&v=4" width = "150" />](https://github.com/zachary-hamilton) | 
|                                [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/JenBanks8585)                                |                            [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/zachary-hamilton)                             |                            
|                [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/jenniferobanks/)                |                 [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/zacharyleehamilton/)                 |    

### [Back End Contributors](https://github.com/Lambda-School-Labs/cityspire-be-h)
|                                                      [Aidan Dang](https://github.com/aidandang)                                                      |
| :-----------------------------------------------------------------------------------------------------------------------------------------: |
| [<img src="https://avatars.githubusercontent.com/u/59453200?s=400&u=b63fe7ed29d4cc93a650433585d987c635f59b20&v=4" width = "150" />](https://github.com/aidandang) |
|                                [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/aidandang)                                |
|                [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/aidandang/)                | 

### [Front End Contributors](https://github.com/Lambda-School-Labs/cityspire-fe-h)    
|                                                      [Jordan Shehane](https://github.com/0neMiss)                                                      |                                                       [Daniel Gipson](https://github.com/dannygipson95)                                      |                                                       [Aidan Dang](https://github.com/aidandang)                                                                
| :-----------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------: |
| [<img src="https://avatars.githubusercontent.com/u/56180519?s=400&u=eaf65cab8a744dc23806afb0cd6458d74dd76721&v=4" width = "150" />](https://github.com/0neMiss) | [<img src="https://avatars.githubusercontent.com/u/63303612?s=400&u=e2ad2ebb68dd3d625fb0fe5a53fba48ec633dc31&v=4" width = "150" />](https://github.com/dannygipson95) | [<img src="https://avatars.githubusercontent.com/u/59453200?s=400&u=b63fe7ed29d4cc93a650433585d987c635f59b20&v=4" width = "150" />](https://github.com/aidandang) |
|                                [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/0neMiss)                                |                            [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/dannygipson95)                             |                            [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/aidandang)                             |                              
|                [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/jordan-shehane-b2807a196/)                |                 [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/daniel-gipson/)                 |                 [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/aidandang/)                 |    
