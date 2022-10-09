### Add sample data




### Data analytics task (Ecommerce data)
- Find top-10 most common first name of the customers from Birmingham
````text
POST /kibana_sample_data_ecommerce/_search
{
    "size": 0,
    "query": {
        "match": {
            "geoip.city_name": "Birmingham"
        }
    },
      "aggs": {
    "name_count": {
      "terms": {
        "field": "customer_first_name.keyword",
        "size": 10
      }
    }
  }
}
````


- What is the busiest day for women buying products cheaper than 75$
````text
POST /kibana_sample_data_ecommerce/_search
{
    "size": 0,
    "query": {
        "bool": {
            "must": [
             {"match": { "customer_gender": "FEMALE" }},
             {"range": {"products.price": {"lte": 75}}}
        ]
        }
    },
    "aggs": {
        "common_day": {
            "terms": {
                "field": "day_of_week"
            }
        }
    }
}
````

- How many products were bought in the last 3 days from Great Britain?
````text

{"size": 0,
    "aggs": {
    "max_date": {                      
      "max": {
        "field": "order_date"
          }
        }
    }
}

{
    "size": 0,
    "query": {
        "bool": {
            "must": [
                {"range": {
                    "order_date": {
                        "lte": "2022-10-22T00:00:00+00:00",
                        "gte": "2022-10-19T00:00:00+00:00"
                        }
                    }
                },
                {"match": {"geoip.country_iso_code": "GB"}}
            ]
        }
    }
}
````

- Standard deviation visualisation of the price with ability to filter by country
````text
{
  "size": 0,
  "query": {
      "match": {
        "geoip.city_name": "Cairo"
      }
  },
  "aggs": {
    "price_average": {
      "avg": {
        "field": "products.price"
      }
    },
    "price_variability": {
      "median_absolute_deviation": {
        "field": "products.price" 
      }
    }
  }
}
````


### Data analytics task (Flightsdata)
- Total distance in miles travelled by all flights
````text
POST /kibana_sample_data_flights/_search
{
    "size": 0,
    "aggs": {
        "total_distance": {
            "sum": {
            "field": "DistanceKilometers"
            }
        }
    }
}
````
- Median price of the flight from Japan, US and Italy
````text
POST /kibana_sample_data_flights/_search
{ "size": 0, 
 "aggs": {
        "JAPAN" : {
            "filter" : { 
              "term": { 
                "OriginCountry": "JP"}},
            "aggs" : {
                "median_price" : { 
                  "median_absolute_deviation" : { 
                    "field" : "AvgTicketPrice" } }
            }},
        "FRANCE": {
            "filter" : { 
              "term": { 
                "OriginCountry": "FR"}},
            "aggs" : {
                "median_price" : { 
                  "median_absolute_deviation" : { 
                    "field" : "AvgTicketPrice" } }
            }
        },
        "ITALY": {
            "filter" : { 
              "term": { 
                "OriginCountry": "IT"}},
            "aggs" : {
                "median_price" : { 
                  "median_absolute_deviation" : { 
                    "field" : "AvgTicketPrice" } }
            }
        }
    }
}
````

- Top-10 most delayed destination airports
````text
{ 
    "size": 0,
    "query": {
        "term": {
            "FlightDelay": true
        }
    },
  "aggs": {
    "by_country_code": {
      "terms": {
        "field": "OriginCountry",
        "size": 10
      },
      "aggs": {
       "delay_sum":  {
          "sum": {
             "field": "FlightDelayMin"
          }
       }
      }
    }
  }
}
````
- Geo map visualisation based on the number of flights from and to the airport
````text
# TODO
````


### Data analytics task (Logsdata)
- Top 5 tags in logs in which contains request to deliver css files
````text
{
    "size": 0,
    "query": {
        "wildcard": {
            "request.keyword":{"value": "*css"}
        }
    },
    "aggs": {
        "tags": {
            "terms": {
                "field": "tags.keyword"
            }
        }
    }
}
````
- What is sum of all RAM for Windows machines that have requests from 6am to 12pm
````text

````
- Find total number of logs with IP in range from 176.0.0.0 to 179.255.255.254
````text

````