# TASK DESCRIPTION:

Develop simple console or web app (up to you) application, that would connect 
to Elasticsearch and would provide ability to use at least 7 different types of 
queries that you either learned in this section or in the Elasticsearch
documentation.

Ideally reuse practice task from module 6 and select appropriate dataset which 
would provide you ability to try several types of queries, not just text, but also 
range and distance


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
ELASTIC_SEARCH_API_ENDPOINT=http://localhost:9200
````

### COMMON FILE EXAMPLE

````python
import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

ELASTIC_SEARCH_API_ENDPOINT = os.getenv('ELASTIC_SEARCH_API_ENDPOINT', 'http://localhost:9200')
````

### MAIN FILE EXAMPLE

````python
import sys
from typing import List

from elasticsearch import Elasticsearch
import argparse
from common import ELASTIC_SEARCH_API_ENDPOINT


def _create_api() -> Elasticsearch:
    """
    Just create Elasticsearch API client
    :return: Elasticsearch
    """
    api = Elasticsearch(ELASTIC_SEARCH_API_ENDPOINT)
    return api


def make_search(api: Elasticsearch, args) -> List[dict]:
    if args.dsl_query_type == 'match_all':
        request = api.search(index=args.index, body={"query": {"match_all": {}}})
        result = request.get('hits', {}).get('hits', [{}])

    elif args.dsl_query_type == 'query_match':
        request = api.search(index=args.index,
                             body={"query": {"match": {args.dsl_field: {"query": args.dsl_query_body}}}})
        result = request.get('hits', {}).get('hits', [{}])

    elif args.dsl_query_type == 'match_phrase':
        request = api.search(index=args.index,
                             body={"query": {"match_phrase": {"query": args.dsl_query_body}}})
        result = request.get('hits', {}).get('hits', [{}])

    elif args.dsl_query_type == 'query_string':
        request = api.search(index=args.index,
                             body={"query": {"query_string": {
                                 "query": args.dsl_query_body,
                                 "default_field": args.dsl_field}}
                             })
        result = request.get('hits', {}).get('hits', [{}])

    elif args.dsl_query_type == 'fuzzy':
        request = api.search(index=args.index,
                             body={"query": {"fuzzy": {
                                 args.dsl_field: {
                                     "value": args.dsl_query_body
                                 }}}
                             })
        result = request.get('hits', {}).get('hits', [{}])

    elif args.dsl_query_type == 'minimum_match':
        request = api.search(index=args.index,
                             body={"query": {
                                 "match": {
                                     args.dsl_field: {
                                         "query": args.dsl_query_body,
                                         "minimum_should_match": args.dsl_min_match_number
                                     }}}})
        result = request.get('hits', {}).get('hits', [{}])
    else:
        result = [{}]

    return result


def main(argv=None):
    api = _create_api()  # Create client

    parser = argparse.ArgumentParser(
        description="Search in ElasticSearch by diff queries")
    parser.add_argument('--index', help='Index for search (default: stdin)',
                        type=str,
                        required=False,
                        default='kibana_sample_data_ecommerce')

    parser.add_argument("--query_type", dest="dsl_query_type", default='match_all', required=False,
                        help="Specify query type")
    parser.add_argument("--query_body", dest="dsl_query_body", default=None, required=False,
                        help="Specify query body")
    parser.add_argument("--field", dest="dsl_field", default='products.product_name', required=False,
                        help="Specify field")

    parser.add_argument("--minimum", dest="dsl_min_match_number", default='1', required=False, type=str,
                        help="Specify minimum match number")

    args = parser.parse_args(argv)
    allowed_types = ['match_all', 'query_match', 'match_phrase', 'query_string', 'fuzzy', 'minimum_match']
    if args.dsl_query_type not in allowed_types:
        parser.print_help()
        sys.exit(1)

    result = make_search(api=api, args=args)
    for item in result:
        print(item['_source'])

    api.close()


if __name__ == '__main__':
    main()

````

### Console Screenshot
<a href='https://postimg.cc/fkwfNcCK' target='_blank'><img src='https://i.postimg.cc/nVmRqTQ6/console-output.jpg' border='0' alt='console-output'/></a>