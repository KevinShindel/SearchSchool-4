# TASK DESCRIPTION

Run Elasticsearch and Kibana
Import sample data available with Elastic stack (ecommerce orders, flight data and web logs)
Complete series of data analytics tasks by writing queries in Kibana or via any programming language SDK

- **Ecommerce data**
````text
How many customers from Birmingham which bought products that costs up to 100$?
How many purchases have double E or double B in their customer’s names?
How many purchases contains only 1 manufacturer, even though there are multiple purchases?
````

- **Flight data**
````text
Number of flights with less than 1000 miles distance
How many flights that do not fly to International airport with Clear and Sunny weather
How many flights were delayed by at least an hour on Monday?
````

- **Web logs**
````text
Number of requests with tags success or login for Windows machines
Find total number of logs with IP in range from 176.0.0.0 to 179.255.255.254 with request size being between 1000 and 10000 bytes
Number of requests with some value of memory field and Firefox based agent
````


## Solution

### How many customers from Birmingham which bought products that costs up to 100$?
````text
POST /kibana_sample_data_ecommerce/_search
{"size": 0, 
  "query": {
    "bool": {
      "must": [
        {"match": {"geoip.city_name": "Birmingham"}},
        {"range": {
          "products.price": {
            "lte": 100
          }
        }}
      ]
    }
  }
}
````
````json
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 326,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  }
}
````

### How many purchases have double E or double B in their customer’s names?
````text
POST kibana_sample_data_ecommerce/_search
{
  "size": 0, 
  "query": {
    "bool": {
      "should": [
        {"wildcard": { "customer_full_name": { "value": "*BB*" }}},
        {"wildcard": { "customer_full_name": { "value": "*EE*" }}}
      ]
    }
  }
}
````
````json
{
  "took" : 2,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 468,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  }
}
````

### How many purchases contains only 1 manufacturer, even though there are multiple purchases?
`````text
POST kibana_sample_data_ecommerce/_search
{
    "size": 0,
    "aggs": {
      "products_cnt": {
        "terms": {
          "field": "products"
        }
      }
    }
}
`````
````json

````

### Number of flights with less than 1000 miles distance
````text
POST kibana_sample_data_flights/_search
{
  "size": 0,
  "query": {
    "range": {
      "DistanceMiles": {
        "gt": 0,
        "lte": 1000
      }
    }
  }
}
````
````json
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1978,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  }
}
````

### How many flights that do not fly to International airport with Clear and Sunny weather
````text
POST kibana_sample_data_flights/_search
{
    "size": 0,
    "query": {
      "bool": {
        "must_not": [{"wildcard": {"Dest": {"value": "*International*"}}}],
        "must": [
          {"terms": {
            "DestWeather": [
              "Clear",
              "Sunny"
            ]
          }}
        ]
      }
    }
}
````
````json
{
  "took" : 7,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1780,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  }
}
````

### How many flights were delayed by at least an hour on Monday?
````text
POST kibana_sample_data_flights/_search
{
    "size": 0,
    "query": {
      "bool": {
        "must": [
          {"match": {"FlightDelay": true}},
          {"match": {"dayOfWeek": 1}},
          {"range": {"FlightDelayMin": {"gte": 60}}}
        ]
      }
    }
}
````
````json
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 403,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  }
}

````

### Number of requests with tags success or login for Windows machines
````text
POST kibana_sample_data_logs/_search
{
    "size": 0,
    "query": {
  "bool": {
        "should": [
          {"term": {"tags.keyword": {"value": "success"}}},
          {"wildcard": {"machine.os.keyword": {"value": "win*"}}}
        ]
      }
    }
}
````
````json
{
  "took" : 10,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 10000,
      "relation" : "gte"
    },
    "max_score" : null,
    "hits" : [ ]
  }
}

````

### Find total number of logs with IP in range from 176.0.0.0 to 179.255.255.254 with request size being between 1000 and 10000 bytes
````text
POST kibana_sample_data_logs/_search
{
    "size": 0,
    "query": {
      "bool": {
        "must": [
          {"term": {"clientip": "176.0.0.0/6"}},
          {"range": {
            "bytes": {
              "gte": 1000,
              "lte": 10000
            }
          }}
        ]
      }
    }
}
````

````json
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 120,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  }
}
````

### Number of requests with some value of memory field and Firefox based agent
````text
POST kibana_sample_data_logs/_search
{
    "size": 0,
    "query": {
    "bool": {
        "must": [
          {"range": {"memory": {"gte": 0}}},
          {"wildcard": {
            "agent.keyword": {
              "value": "Mozilla*"
            }
          }}
        ]
      }
    }
}
````
````json
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 552,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  }
}
````
