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
        "field": "customer_first_name"
      }
    }
  }
}
````

# TODO: Resolve error
````text
 "caused_by": {
      "type": "illegal_argument_exception",
      "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [customer_first_name] in order to load field data by uninverting the inverted index. Note that this can use significant memory.",
      "caused_by": {
        "type": "illegal_argument_exception",
        "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [customer_first_name] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
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

````

- Standard deviation visualisation of the price with ability to filter by country
````text

````


### Data analytics task (Flightsdata)
- Total distance in miles travelled by all flights
- Median price of the flight from Japan, US and Italy
- Top-10 most delayed destination airports
- Geo map visualisation based on the number of flights from and to the airport


### Data analytics task (Logsdata)
- Top 5 tags in logs in which contains request to deliver css files
- What is sum of all RAM for Windows machines that have requests from 6am to 12pm
- Find total number of logs with IP in range from 176.0.0.0 to 179.255.255.254