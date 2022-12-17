import json

from common import _create_api, _create_index
from elasticsearch.helpers import bulk


def upload():
    index = 'movie-csv'
    api = _create_api()
    _create_index(api, index)

    with open('result.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    created, _ = bulk(client=api, index=index, actions=data)


if __name__ == '__main__':
    upload()
