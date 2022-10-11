# TASK DESCRIPTION:
Write simple indexing application in your language of choice – Java/Python/C#/Javascript/etc...
which will index simple csv file

### CSV FILE EXAMPLE
<a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/DZPB6ryV/csv-file.jpg' border='0' alt='csv-file'/></a>

### DOCKER FILE EXAMPLE
````dockerfile
version: "3.3"
services:
  elasticsearch:
    image: elasticsearch:7.16.3
    ports:
      - "9200:9200"
      - "9300:9300"
    environment:
        - http.host=0.0.0.0
        - transport.host=0.0.0.0
        - "ES_JAVA_OPTS=-Xms1g -Xmx1g "
        - cluster.name=elk-docker-cluster
        - node.name=elk-docker-single-node
        - http.cors.enabled=true
        - http.cors.allow-origin=*
        - xpack.ml.enabled=false
        - discovery.type=single-node

  kibana:
    image: kibana:7.16.3
    depends_on:
    - elasticsearch
    restart: on-failure
    links:
    - elasticsearch
    ports:
      - "5601:5601"

````
### ENV FILE 
````yaml
FILE=access-code-password-recovery-code.csv
ELASTIC_SEARCH_API_ENDPOINT=http://localhost:9200
````

### COMMON FILE EXAMPLE
````python
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

FILE = os.getenv('FILE', 'access-code-password-recovery-code.csv')
ELASTIC_SEARCH_API_ENDPOINT = os.getenv('ELASTIC_SEARCH_API_ENDPOINT', 'http://localhost:9200')

TEST_DOC = {'access_code': '12se74',
            'recovery_code': 'rb9012',
            'first_name': 'Rachel',
            'last_name': 'Booker',
            'department': 'Sales',
            'location': 'Manchester',
            'created': '2022-10-11T20:24:30.586918'}

````
### MAIN FILE EXAMPLE
````python
from csv import DictReader
from typing import Iterable

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from common import ELASTIC_SEARCH_API_ENDPOINT, FILE, TEST_DOC


def _create_api() -> Elasticsearch:
    """
    Just create Elasticsearch API client
    :return: Elasticsearch
    """
    api = Elasticsearch(ELASTIC_SEARCH_API_ENDPOINT)
    return api


def _get_data(filepath: str) -> Iterable:
    """
    Open CSV file and yield from
    :param filepath: string
    :return: Iterable
    """
    reader = open(file=filepath, mode='r', encoding='utf-8')
    csv_reader = DictReader(reader)
    yield from csv_reader


def _create_index(client) -> None:
    """
    Create Index with mapping
    :param client: Elasticsearch
    :return: None
    """
    client.indices.create(
        index="demo-csv",
        body={
            "settings": {"number_of_shards": 1},
            "mappings": {
                "properties": {
                    "access_code": {"type": "keyword"},
                    "recovery_code": {"type": "keyword"},
                    "first_name": {"type": "keyword"},
                    "last_name": {"type": "keyword"},
                    "department": {"type": "keyword"},
                    "location": {"type": "keyword"},
                    "created": {"type": "date"},
                }
            },
        },
        ignore=400,
    )


def main():
    api = _create_api()  # Create client
    _create_index(client=api)  # Create index
    index = 'demo-csv'  # Index name
    data = _get_data(FILE)  # get iterated data from csv file
    created, _ = bulk(client=api, index=index, actions=data)  # bulk creation from file
    document = api.get(index=index, id='901242')  # Get created document
    assert document.body['_source'] == TEST_DOC   # Check created document with tested
    queryset = api.search(index=index)  # Get all created documents
    assert queryset.body['hits']['total']['value'] is created  # check quantity len
    api.indices.delete(index=index)  # Drop index with documents
    print(api.info())  # Show Elasticsearch


if __name__ == '__main__':
    main()

````

### Kibana Screenshot
<a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/BvgKwMDC/data.jpg' border='0' alt='data'/></a>