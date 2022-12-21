# Task
Consume HTTP API continuously - https://api2.binance.com/api/v3/ticker/24hr
Split data for each individual symbol. E.g., "symbol":"LUNCUSDT"
Represents pair of currencies. E.g., LUNC to USDT. 
Index each separate event into Elasticsearch into index based on current hour. 
Let pipeline work with saving data for the last 7 days
Add any extra info to the events



# Task list

1. Investigate HTTP Request
2. Create Logstash configuration
3. Create Dockerfile
4. Create Docker Compose file
5. Run Docker 
6. Check Kibana for result

# Solution

1. Check for HTTP data
<a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/mgcKVZsS/1.jpg' border='0' height="250px" alt='1'/></a>

2. Logstash config file
````text
input {
   pipe {
    command => 'curl "https://api2.binance.com/api/v3/ticker/24hr"' # get data from HTTP 
    codec => "json" # use json codec
  }
}


filter {

    json {
        source => "message"
    }

     mutate {
        remove_field => [ "command", "host" ] # remove command and host fields
        convert => { # convert text fields into float
          "bidQty" => "float"
          "volume" => "float"
          "priceChangePercent" => "float"
          "quoteVolume" => "float"
          "prevClosePrice" => "float"
          "highPrice" => "float"
          "lowPrice" => "float"
          "lastPrice" => "float"
          "askQty" => "float"
          "askPrice" => "float"
          "bidPrice" => "float"
          "openPrice" => "float",
          "weightedAvgPrice" => "float",
          "lastQty" => "float"
        }
        gsub => [
          "symbol", ".+USD+.", "USD", # use regex for replace text
    ]
    }
}

output {

     stdout { codec => rubydebug } # show up in console

    elasticsearch {
        hosts => ["elasticsearch:9200"] # output to elasticsearch
        index => "binance-%{+YYYY.MM.dd-HH}" # create index every hours
    }
}
````

3. Dockerfile for Logstash
````dockerfile
FROM logstash:6.4.0
ADD /config/http-pipeline.conf /usr/share/logstash/config
ADD /config/logstash.yml /usr/share/logstash/config
CMD logstash -f /usr/share/logstash/config/http-pipeline.conf
````

4. DockerCompose file
````dockerfile
version: "3.3"
services:

  logstash:
    build: .
    container_name: logstash
    depends_on:
      - elasticsearch
    restart: always
    environment:
      LOGSPOUT: ignore
    ports:
      - "5000:5000"
    links:
      - elasticsearch

  elasticsearch:
    container_name: elasticsearch
    image: elasticsearch:6.4.0
    volumes:
      - ./elk.conf.yml:/usr/share/elasticsearch/config/elasticsearch.yml
    environment:
      LOGSPOUT: ignore
        - http.host=0.0.0.0
        - transport.host=0.0.0.0
        - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
    ports:
      - "9200:9200"
      - "9300:9300"

  kibana:
    image: kibana:6.4.0
    container_name: kibana
    environment:
      LOGSPOUT: ignore
      ELASTICSEARCH_URL: http://elasticsearch:9200
    links:
      - elasticsearch
    ports:
      - "5601:5601"

````

5. Run docker
````shell
docker-compose build
docker-compose up
````
<a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/zG0Y22bJ/Search-School-4-http-pipeline-conf-2022-12-20-19-36-18.gif' border='0' alt='Search-School-4-http-pipeline-conf-2022-12-20-19-36-18'/></a>

6. Check Kibana

<a href='https://postimg.cc/p9VqKJfR' target='_blank'><img src='https://i.postimg.cc/R0Ky5Pq6/2.jpg' border='0' height="250px" alt='2'/></a>
<a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/kGBy94w1/3.jpg' border='0' height="400px" alt='3'/></a>
<a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/s2mPhSNH/4.jpg' border='0' height="400px" alt='4'/></a>