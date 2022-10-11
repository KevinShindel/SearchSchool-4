from datetime import datetime
from typing import Iterable
from urllib.parse import urlparse, ParseResultBytes, ParseResult

from elasticsearch import Elasticsearch
from csv import DictReader
from common import ELASTIC_SEARCH_API_ENDPOINT, FILE


def _create_api() -> Elasticsearch:
    schema = _get_url_schema(ELASTIC_SEARCH_API_ENDPOINT)

    api = Elasticsearch(
        [schema.scheme+"://"+schema.hostname+":"+str(schema.port)],
        http_auth=(schema.username, schema.password))
    return api


def _get_data(filepath: str) -> Iterable:
    reader = open(file=filepath, mode='r', encoding='utf-8')
    csv_reader = DictReader(reader)
    yield from csv_reader


def _get_url_schema(url: str) -> ParseResult:
    schema = urlparse(url=url)
    return schema


def main():
    api = _create_api()

    api.create()


if __name__ == '__main__':
    main()
