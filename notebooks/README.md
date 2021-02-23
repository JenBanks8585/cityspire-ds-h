# CitySpire DS API 
## Link
* [DS API](https://h-ds2.cityspire.dev/)
## Framework
* FastAPI, deployed on AWS Elastic Beanstalk
## Endpoints
* ## Database
 `/city_list` : Returns a list of all cities that are in the database returns city_name and state_name
 `/state_list`: Returns a list of all states that are in the database returns state_name and state_abbreviation
 `/location`: 
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