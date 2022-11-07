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
