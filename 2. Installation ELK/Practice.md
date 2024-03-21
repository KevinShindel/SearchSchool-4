### Data analytics task (Ecommerce data)

- Find top-10 most common first name of the customers from Birmingham

<a href="https://postimg.cc/Cdsyt7Gh" target="_blank"><img src="https://i.postimg.cc/44rJYFn9/4.jpg" alt="4"/></a><br/><br/>
<a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/nLHVHjrS/1-1.jpg' border='0' alt='1-1'/></a>

````text
POST /kibana_sample_data_ecommerce/_search
````

````json
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

- What is the busiest day for women buying products cheaper than
  <a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/prTQFLTP/2-1.jpg' border='0' alt='2-1'/></a>

````text
POST /kibana_sample_data_ecommerce/_search
````

````json
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "customer_gender": "FEMALE"
          }
        },
        {
          "range": {
            "products.price": {
              "lte": 75
            }
          }
        }
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

<a href="https://postimg.cc/bsm7YvV4" target="_blank"><img src="https://i.postimg.cc/pLvRZhfV/5.jpg" alt="5"/></a><br/><br/>

````text
POST /kibana_sample_data_ecommerce/_search
````

````json
{
  "size": 0,
  "aggs": {
    "max_date": {
      "max": {
        "field": "order_date"
      }
    }
  }
}
````

````json
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "order_date": {
              "lte": "2022-10-22T00:00:00+00:00",
              "gte": "2022-10-19T00:00:00+00:00"
            }
          }
        },
        {
          "match": {
            "geoip.country_iso_code": "GB"
          }
        }
      ]
    }
  }
}
````

- Standard deviation visualisation of the price with ability to filter by country

<a href="https://postimg.cc/ts7LsHLJ" target="_blank"><img src="https://i.postimg.cc/sgJy0jmY/5-1.jpg" alt="5-1"/></a><br/><br/>

````json
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

<a href="https://postimg.cc/jLqVrfcz" target="_blank"><img src="https://i.postimg.cc/MKVzVbjr/6.jpg" alt="6"/></a><br/><br/>

````text
POST /kibana_sample_data_flights/_search
````

````json
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

- Median price of the flight from Japan, US and

<a href="https://postimg.cc/hXwNx5Br" target="_blank"><img src="https://i.postimg.cc/k5XC00Yk/7.jpg" alt="7"/></a><br/><br/>

````text
POST /kibana_sample_data_flights/_search
````

````json
{
  "size": 0,
  "aggs": {
    "JAPAN": {
      "filter": {
        "term": {
          "OriginCountry": "JP"
        }
      },
      "aggs": {
        "median_price": {
          "median_absolute_deviation": {
            "field": "AvgTicketPrice"
          }
        }
      }
    },
    "FRANCE": {
      "filter": {
        "term": {
          "OriginCountry": "FR"
        }
      },
      "aggs": {
        "median_price": {
          "median_absolute_deviation": {
            "field": "AvgTicketPrice"
          }
        }
      }
    },
    "ITALY": {
      "filter": {
        "term": {
          "OriginCountry": "IT"
        }
      },
      "aggs": {
        "median_price": {
          "median_absolute_deviation": {
            "field": "AvgTicketPrice"
          }
        }
      }
    }
  }
}
````

- Top-10 most delayed destination airports

<a href="https://postimg.cc/30KqYMXK" target="_blank"><img src="https://i.postimg.cc/Rhfx14qn/8.jpg" alt="8"/></a><br/><br/>

````text
POST /kibana_sample_data_flights/_search
````

````json
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
        "delay_sum": {
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

<a href='https://postimg.cc/gLmWRZvb' target='_blank'><img src='https://i.postimg.cc/qqCMPcqq/fly-map.jpg' border='0' alt='fly-map'/></a>

### Data analytics task (Logsdata)

- Top 5 tags in logs in which contains request to deliver css files

<a href="https://postimg.cc/MMJ43fXf" target="_blank"><img src="https://i.postimg.cc/rmDkmSkj/9.jpg" alt="9"/></a><br/><br/>
<a href="https://postimg.cc/7G1RFPTs" target="_blank"><img src="https://i.postimg.cc/Y9Twmh2H/10.jpg" alt="10"/></a><br/><br/>

````json
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

<a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/L5DCd8CP/total-ram.jpg' border='0' alt='total-ram'/></a>

````json
{
  "size": 0,
  "query": {
    "constant_score": {
      "filter": {
        "bool": {
          "must": [
            {
              "script": {
                "script": {
                  "source": "doc['timestamp'].value.getHour() >= params.min && doc['timestamp'].value.getHour() <= params.max",
                  "params": {
                    "min": 6,
                    "max": 24
                  }
                }
              }
            },
            {
              "wildcard": {
                "machine.os": {
                  "value": "win*"
                }
              }
            }
          ]
        }
      }
    }
  },
  "aggs": {
    "total_RAM": {
      "sum": {
        "field": "machine.ram"
      }
    }
  }
}
````

- Find total number of logs with IP in range from 176.0.0.0 to 179.255.255.254

<a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/V6RBvHqQ/ip-submask.jpg' border='0' alt='ip-submask'/></a>
<a href='https://postimg.cc/s1gGG6JX' target='_blank'><img src='https://i.postimg.cc/y6Fm52gF/client-ip.jpg' border='0' alt='client-ip'/></a>
````json
{
    "size": 0,
    "query": {
        "term": {
            "clientip": "176.0.0.0/6"
        }
    }
}
````