# TASK DESCRIPTION:
## Index movie lens content to Elasticsearch
https://files.grouplens.org/datasets/movielens/ml-25m-README.html
(movies.csv, ratings.csv, tags.csv)

You could use any way to index data:
- Logstash (csv input, … )
- Java/Python/C# – Elastic client -> indexing
````text
Console application – which search movies (match phrase, fuzzy, filter/sort by average 
rating, finding top-10 tags for the movie, find movies which userX is put rating of 5).
Try implement it using several approaches for working with hierarchical data and explain 
which one is the beat fit here
````


## Solution

### Movie Data Example

````json
{
  "movieId": 1,
  "title": "Toy Story (1995)",
  "genres": "Adventure|Animation|Children|Comedy|Fantasy",
  "rating": [
    {
      "value": 4.0,
      "timestamp": 964982703,
      "userId": 336
    },
    {
      "value": 4.0,
      "timestamp": 847434962,
      "userId": 474
    }
  ],
  "tag": [
    {
      "value": "pixar",
      "userId": 336,
      "timestamp": 1139045764
    }
  ]
}
````
### Index Schema example
````json
{
  "mappings": {
    "properties": {
      "movieId": {"type": "integer"},
      "title": {"type": "text"},
      "genres": {"type": "keyword"},
      "rating": {"type": "nested"},
      "tag": {"type": "nested"}
    }
  }
}
````

### Merge data with pandas
````python
import json

from pandas import read_csv, merge, Series


def collect_to_dict(series: Series, keys: list):
    data = [dict(zip(keys, item)) for item in tuple(zip(*series.values))]
    return data


def main():
    movies_df = read_csv('movies.csv')
    tags_df = read_csv('tags.csv', names=['tag_user_id', 'movieId', 'tag_value', 'tag_timestamp'], skiprows=1)
    ratings_df = read_csv('ratings.csv', names=['rating_user_id', 'movieId', 'rating_value', 'rating_timestamp'], skiprows=1)

    movie_w_tags_df = merge(left=movies_df, right=tags_df, how='left', on='movieId')\
        .groupby(['movieId', 'title', 'genres'])\
        .agg({'tag_user_id': list, 'tag_value': list, 'tag_timestamp': list}).reset_index()

    final_df = merge(left=movie_w_tags_df, right=ratings_df, on='movieId', how='left')\
        .groupby(['movieId', 'title', 'genres'])\
        .agg({'rating_user_id': list, 'rating_value': list, 'rating_timestamp': list, 'tag_user_id': 'first', 'tag_value': 'first', 'tag_timestamp': 'first'}).reset_index()

    rating_columns = ['userId', 'value', 'timestamp']
    final_df['rating'] = final_df[['rating_user_id', 'rating_value', 'rating_timestamp']].apply(lambda df: collect_to_dict(df, rating_columns), axis=1)

    tags_columns = ['userId', 'value', 'timestamp']
    final_df['tag'] = final_df[['tag_user_id', 'tag_value', 'tag_timestamp']].apply(lambda df: collect_to_dict(df, tags_columns), axis=1)

    records = final_df[['movieId', 'title', 'genres', 'rating', 'tag']].to_dict('records')

    with open('result.json', 'w') as handler:
        handler.write(json.dumps(records, indent=4))
````

### Upload data to ELK
````python
import json
import os
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

ELASTIC_SEARCH_API_ENDPOINT = os.getenv('ELASTIC_SEARCH_API_ENDPOINT', 'http://localhost:9200')


def _create_api() -> Elasticsearch:
    """
    Just create Elasticsearch API client
    :return: Elasticsearch
    """
    return Elasticsearch(ELASTIC_SEARCH_API_ENDPOINT)


def _create_index(client, index) -> None:
    """
    Create Index with mapping
    :param client: Elasticsearch
    :return: None
    """
    client.indices.create(
        index=index,
        body={
            "settings": {"number_of_shards": 1},
            "mappings": {
                "properties": {
                    "movieId": {"type": "integer"},
                    "title": {"type": "text"},
                    "genres": {"type": "keyword"},
                    "rating": {"type": "nested"},
                    "tag": {"type": "nested"},
                }
            },
        },
        ignore=400,
    )


def upload():
    index = 'movie-csv'
    api = _create_api()
    _create_index(api, index)

    with open('result.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    created, _ = bulk(client=api, index=index, actions=data)
````
### Uploaded data in ELK index
<a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/sXnTcwpQ/data.jpg' border='0' alt='data' height="400px" width="auto"/></a>

### Search Console implementation
````python
import sys, os
from typing import List

from elasticsearch import Elasticsearch
import argparse

ELASTIC_SEARCH_API_ENDPOINT = os.getenv('ELASTIC_SEARCH_API_ENDPOINT', 'http://localhost:9200')


def _create_api() -> Elasticsearch:
    """
    Just create Elasticsearch API client
    :return: Elasticsearch
    """
    return Elasticsearch(ELASTIC_SEARCH_API_ENDPOINT)


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
````

<a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/qMBxqzRg/data.jpg' border='0' alt='data'/></a>

1. Search by match phrase
````text
POST /movie-csv/_search
````
````json
{
  "size": 0,
    "query": {
    "match": {
      "title": "Star Wars"
    }
    },
  "aggs": {
    "by_movie_id": {
      "terms": {
        "field": "movieId"
      },
      "aggs": {
        "nested_rating_agg": {
          "nested": {
            "path": "rating"
          },
          "aggs": {
            "avg_rating": {
              "avg": {
                "field": "rating.value"
              }
            }
          }
        }
      }
    }
  }
}
````
2. Sort by aggregated field
````text
POST /movie-csv/_search
````
````json
{
  "size": 0,
  "query": {
    "match": {
      "title": "Star Wars"
    }
  },
  "aggs": {
    "nested_rating_agg": {
      "nested": {
        "path": "rating"
      },
      "aggs": {
        "avg_rating": {
          "avg": {
            "field": "rating.value"
          }
        },
        "avg_rating_sort": {
          "bucket_sort": {
            "sort": [
              { "avg_rating": { "order": "desc" } } 
            ]
          }
        }
      }
    }
  }
}
````

output
````json
{
  "error" : {
    "root_cause" : [ ],
    "type" : "search_phase_execution_exception",
    "reason" : "",
    "phase" : "fetch",
    "grouped" : true,
    "failed_shards" : [ ],
    "caused_by" : {
      "type" : "class_cast_exception",
      "reason" : "class org.elasticsearch.search.aggregations.bucket.nested.InternalNested cannot be cast to class org.elasticsearch.search.aggregations.InternalMultiBucketAggregation (org.elasticsearch.search.aggregations.bucket.nested.InternalNested and org.elasticsearch.search.aggregations.InternalMultiBucketAggregation are in unnamed module of loader 'app')"
    }
  },
  "status" : 500
}

````

3. Filter by avg rating
````text
POST /movie-csv/_search
````
````json
{
  "size": 0,
  "query": {
    "match": {
      "title": "Star Wars"
    }
  },
  "aggs": {
    "nested_rating_agg": {
      "nested": {
        "path": "rating"
      },
      "aggs": {
        "avg_rating": {
          "avg": {
            "field": "rating.value"
          }
        }
      }, "over_rating": {"filter": {"range": { "avg_rating": {"gte": 3}}}}
    }
  }
}
````