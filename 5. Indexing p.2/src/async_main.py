from csv import DictReader
from typing import Iterable
import asyncio

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
import logging

from common import ELASTIC_SEARCH_API_ENDPOINT, FILE, TEST_DOC

logger = logging.getLogger('Elastic')


async def _async_create_api() -> AsyncElasticsearch:
    client = AsyncElasticsearch(ELASTIC_SEARCH_API_ENDPOINT)
    return client


async def _async_get_data(index, filepath: str) -> Iterable:
    """
    Open CSV file and yield from
    :param filepath: string
    :return: Iterable
    """
    reader = open(file=filepath, mode='r', encoding='utf-8')
    csv_reader = DictReader(reader)
    data = map(lambda i: {'_index': index, '_doc': i, '_id': i.pop('_id')}, csv_reader)
    return data


async def _async_create_index(client: AsyncElasticsearch) -> None:
    """
    Create Index with mapping
    :param client: Elasticsearch
    :return: None
    """
    await client.indices.create(
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


async def async_main():
    client = await _async_create_api()
    logger.info(msg='[+] Client connected!')
    logger.info(msg=client.info)
    index = 'async-demo-csv'
    actions = await _async_get_data(index=index, filepath=FILE)
    await _async_create_index(client=client)
    logger.info(msg=f'[+] Index: {index} created...')
    created, _ = await async_bulk(client=client, actions=actions)
    logger.info(f'[!] Total created: {created} records...')

    document = await client.get(index=index, id='901242')  # Get created document
    assert document.body['_source']['_doc'] == TEST_DOC  # Check created document

    queryset = await client.search(index=index, query={"match_all": {}})
    records_created = queryset.body['hits']['total']['value']
    logger.info(msg=f'[!] Found {records_created} records')
    assert records_created is created

    await client.indices.delete(index=index)
    await client.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())
