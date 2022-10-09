GET _/_cat/indices_ <- show all indexes

/_cat/indices?v <- Formatted output

/_cat/health?v <- Show current status of cluster

/_cat/nodes?v <- Show all nodes

PUT /sales <- create new index

PUT /sales/order/123 {"order_id": 123, "order_amount": 100} <- Add new document

GET /sales/order/123 <- Get created document

DELETE /sales/order/123 <- Get created document

# Load from CURL
curl -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/_bulk --data-binary "@reqs"; echo

````shell
curl -H 'Content-Type: application/x-ndjson' -XPOST 'localhost:9200/bank/account/_bulk?pretty' --data-binary @accounts.json
````

### Bulk create via console
````shell
PUT /bank
POST /bank/_bulk {{data from accounts.json}}
````

### Get all records
````text
GET bank/account/_search
````

### Simple query 
````text
POST /bank/account/_search
{
  "query": {
    "match": {
      "state": "CA"
    }
  }
}
````
### Search by few conditions ( find records in CA and female state)
````text
POST /bank/account/_search
{
  "query": {
      "bool": {
          "must": [
            {"match": { "state": "CA"}},
            {"match": { "gender": "F"}}
          ]
      }
  }
}
````

### Search with logical OR (CA of female)
````text
{
  "query": {
      "bool": {
          "should": [
            {"match": { "state": "CA"}},
            {"match": { "gender": "F"}}
          ]
      }

  }
}
````

### Search numeric (find account 516)
````text
{
  "query": {
    "term": {"account_number": 516}
  }
}
````

### Inclusion numeric select
````text
{
  "query": {
    "terms": { "account_number": [516, 802] }
  }
}
````

### Range numeric searching (account number between 100 and 200)
````text
{
  "query": {
    "range": { "account_number": {
        "gte": 100,
        "lte": 200
    }}
  }
}
````

### Sorting (greater then 35 age old, and sorting ascending)
````text
{
  "query": {
    "range": { "age": {
        "gte": 35
    }}
  }, 
    "sort": {
        "age": {"order": "asc"}
    }
}
````

### Mapping and tokenization
````text
GET bank/_analyze
{
  "tokenizer" : "letter",
  "text" : "The Moon-is-Made of Cheese.Some Say$"
}
````

### URL parsing
````text
GET bank/_analyze
{
  "tokenizer": "uax_url_email",
  "text": "you@example.com login at https://bensullins.com attempt"
}

````

### Create mapping with tokenization
````text
PUT /idx1
{
  "mappings": {
    "t1": {
      "properties": {
        "title": {
            "type": "text",
            "analyzer" : "standard"
        },
        "english_title": {
            "type":     "text",
            "analyzer": "english"
        }
      }
    }
  }
}

````

### Check mapping
````text
GET idx1

GET idx1/_analyze
{
  "field": "title",
  "text": "Bears"
}

GET idx1/_analyze
{
  "field": "english_title",
  "text": "Bears"
}
````


## Aggregation
```text
{
    "size": 0,
    "aggs": {
        "AGGREGATION_NAME": {
            "terms": {
                "field": "GROUP_BY_FIELDNAME"
            }
        }
    },
    "sort": { "SORTING_FIELD_NAME": {"order": "asc"} }
}
```
### Aggregation with grouping by [state.keyword] field
```text
POST bank/account/_search
{
  "size": 0,
  "aggs": {
    "states": {
      "terms": {
        "field": "state.keyword"
      }
    }
  }
}
```
### Group by [state.keyword] and calculate average [balance] 
```text
GET bank/account/_search
{
  "size": 0,
  "aggs": {
    "states": {
      "terms": {
        "field": "state.keyword"
      },
      "aggs": {
        "avg_bal": {
          "avg": {
            "field": "balance"
          }
        }
      }
    }
  }
}
```

### Show stats 
````text
{
  "size": 0,
  "aggs": {
    "balance-stats": {
      "stats": {
        "field": "balance"
      }
    }
  }
}
````

### Filtering and Aggregation ( count only CA states )
````text
{
  "size": 0,
  "query": {
    "match": {
      "state.keyword": "CA"
    }
  },
  "aggs": {
    "states": {
      "terms": {
        "field": "state.keyword"
      }
    }
  }
}
````

### Aggregation with mulltiple filtration
````text
{
  "size": 0,
  "query": {
      "bool": {
          "must": [
            {"match": { "state.keyword": "CA" }},
            {"range": {"age":{"lte": 25}}}
          ]
      }
    
  },
  "aggs": {
    "states": {
      "terms": {
        "field": "state.keyword"
      }
    }
  }
}
````

### Filter by state then filter by age and group by
````text
{
  "size": 0,
  "query": {
    "match": {"state.keyword": "CA"}
  },
  "aggs": {
    "over35":{
      "filter": {
        "range": {"age": {"gt": 35}}
      },
    "aggs": {"avg_bal": {"avg": {"field": "balance"} }}
    }
  }
}
````

### Look at state avg and global average
````text
GET bank/account/_search
{
  "size": 0,
  "aggs": {
    "state_avg": {
      "terms": {
        "field": "state.keyword"
      },
      "aggs": {"avg_bal": {"avg": {"field": "balance"}}}
    },
    "global_avg": {
      "global": {},
      "aggs": {"avg_bal": {"avg": {"field": "balance"}}}
    }
  }
}
````

### Look at the percentiles for the balances
````text
GET bank/account/_search
{
  "size": 0,
  "aggs": {
    "pct_balances": {
      "percentiles": {
        "field": "balance",
        "percents": [
          1,
          5,
          25,
          50,
          75,
          95,
          99
        ]
      }
    }
  }
}
````


### Can also calculate High Dynamic Range (HDR) Historgram

````text
GET bank/account/_search
{
  "size": 0,
  "aggs": {
    "pct_balances": {
      "percentiles": {
        "field": "balance",
        "percents": [
          1,
          5,
          25,
          50,
          75,
          95,
          99
        ],
        "hdr": {
          "number_of_significant_value_digits": 3
        }
      }
    }
  }
}
````


### We can use the percentile ranks agg for checking a individual values
````text
GET bank/account/_search
{
  "size": 0,
  "aggs": {
    "bal_outlier": {
      "percentile_ranks": {
        "field": "balance",
        "values": [35000,50000],
        "hdr": {
          "number_of_significant_value_digits": 3
        }
      }
    }
  }
}
````


### Similarly we can create a histogram
````text
GET bank/account/_search
{
  "size": 0,
  "aggs": {
    "bals": {
      "histogram": {
        "field": "balance",
        "interval": 500
      }
    }
  }
}
````

