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
