# Task
Consume HTTP API continuously - https://api2.binance.com/api/v3/ticker/24hr
Split data for each individual symbol. E.g., "symbol":"LUNCUSDT"
Represents pair of currencies. E.g., LUNC to USDT. 
Index each separate event into Elasticsearch into index based on current hour. 
Let pipeline work with saving data for the last 7 days
Add any extra info to the events

# Solution

# TODO: Create docker container with Logstash + Kibana + ElasticSearch
1. Investigate Logstash HTTP client
2. Create schema for retrieve data to Logstash
3. Create link Logstash + Kibana + ElasticSearch

### Create logstash configuration and save as  http-pipeline.conf

`````text
input {
 http {
    host => "https://api2.binance.com/api/v3/ticker/24hr"
    port => "443"
  }
}


filter {
    json {
        source => "message"    
    }
}

output {

     stdout { codec => rubydebug }
    
     file {
        path => "/log_streaming/http-pipeline/http-pipeline.log"
    }
    
    elasticsearch {
        host => "localhost"
        index => "binance"
    }
}
`````

### Example of data

````json
{
  "symbol": "ETHBTC",
  "priceChange": "0.00135200", 
  "priceChangePercent": "1.907",
  "weightedAvgPrice": "0.07149529",
  "prevClosePrice": "0.07089000",
  "lastPrice": "0.07223400", 
  "lastQty": "7.63940000", 
  "bidPrice": "0.07223400",
  "bidQty": "16.60500000", 
  "askPrice": "0.07223500",
  "askQty": "23.44040000",
  "openPrice": "0.07088200",
  "highPrice": "0.07235000",
  "lowPrice": "0.07044700",
  "volume": "38290.72530000",
  "quoteVolume": "2737.60634021",
  "openTime": 1671453765946,
  "closeTime": 1671540165946, 
  "firstId": 394731009, 
  "lastId": 394807597,
  "count": 76589
}
````

### Create ELK Index
````text
PUT /binance
````
````json
{
  "mappings": {
    "properties": {
      "symbol": {"type": "keyword"},
      "priceChange": {"type": "double"},
      "priceChangePercent": {"type": "double"},
      "weightedAvgPrice": {"type": "double"},
      "prevClosePrice": {"type": "double"},
      "lastPrice": {"type": "double"},
      "lastQty": {"type": "double"},
      "bidPrice": {"type": "double"},
      "bidQty": {"type": "double"},
      "askPrice": {"type": "double"},
      "openPrice": {"type": "double"},
      "highPrice": {"type": "double"},
      "lowPrice": {"type": "double"},
      "volume": {"type": "double"},
      "quoteVolume": {"type": "double"},
      "openTime": {"type": "date"},
      "closeTime": {"type": "date"},
      "firstId": {"type": "integer"},
      "lastId": {"type": "double"},
      "count": {"type": "double"}
    }
  }
}
````

### Test create one record
````text
POST binance/_doc/1
````
````json
{
  "symbol": "ETHBTC",
  "priceChange": "0.00135200", 
  "priceChangePercent": "1.907",
  "weightedAvgPrice": "0.07149529",
  "prevClosePrice": "0.07089000",
  "lastPrice": "0.07223400", 
  "lastQty": "7.63940000", 
  "bidPrice": "0.07223400",
  "bidQty": "16.60500000", 
  "askPrice": "0.07223500",
  "askQty": "23.44040000",
  "openPrice": "0.07088200",
  "highPrice": "0.07235000",
  "lowPrice": "0.07044700",
  "volume": "38290.72530000",
  "quoteVolume": "2737.60634021",
  "openTime": 1671453765946,
  "closeTime": 1671540165946, 
  "firstId": 394731009, 
  "lastId": 394807597,
  "count": 76589
}


````

### Get created document
````text
GET binance/_doc/1
````