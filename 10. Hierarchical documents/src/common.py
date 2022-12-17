import os
from elasticsearch import Elasticsearch
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

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
