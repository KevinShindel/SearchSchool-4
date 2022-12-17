import sys
from typing import List

from elasticsearch import Elasticsearch
import argparse
from common import _create_api


def make_search(api: Elasticsearch, args) -> List[dict]:
    if args.dsl_query_type == 'match':
        request = api.search(index=args.index,
                             body={"query": {"match": {args.dsl_field: {"query": args.dsl_query_body}}}})
        result = request.get('hits', {}).get('hits', [{}])

    elif args.dsl_query_type == 'match_phrase':
        request = api.search(index=args.index,
                             body={"query": {"match_phrase": {"query": args.dsl_query_body}}})
        result = request.get('hits', {}).get('hits', [{}])

    elif args.dsl_query_type == 'fuzzy':
        request = api.search(index=args.index,
                             body={"query": {"fuzzy": {
                                 args.dsl_field: {
                                     "value": args.dsl_query_body
                                 }}}
                             })
        result = request.get('hits', {}).get('hits', [{}])

    elif args.dsl_query_type == 'filter_avg':
        request = api.search(index=args.index,
                             body={"query": {
                                 "match": {
                                     args.dsl_field: {
                                         "query": args.dsl_query_body,
                                         "minimum_should_match": args.dsl_min_match_number
                                     }}}})
        result = request.get('hits', {}).get('hits', [{}])

    # TODO: Implement top
    # TODO: Implement top_by_user
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
                        default='movie-csv')

    parser.add_argument("--query_type", dest="dsl_query_type", default='match', required=False,
                        help="Specify query type")
    parser.add_argument("--query_body", dest="dsl_query_body", default=None, required=False,
                        help="Specify query body")
    parser.add_argument("--field", dest="dsl_field", default='rating.value', required=False,
                        help="Specify field")

    parser.add_argument("--minimum", dest="dsl_required_rating", default='1', required=False, type=str,
                        help="Specify minimum match number")

    args = parser.parse_args(argv)
    # (match phrase, fuzzy, filter/sort by average
    # rating, finding top-10 tags for the movie, find movies which userX is put rating of 5)
    allowed_types = ['match', 'match_phrase', 'fuzzy', 'filter_avg', 'sort_avg', 'top', 'top_by_user']
    if args.dsl_query_type not in allowed_types:
        parser.print_help()
        sys.exit(1)

    result = make_search(api=api, args=args)
    for item in result:
        print(item['_source'])

    api.close()


if __name__ == '__main__':
    main()
