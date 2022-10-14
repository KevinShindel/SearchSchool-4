import os
import time

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


def time_wrapper(*args, **kwargs):
    def wrapper(fn):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        end = time.perf_counter()
        elapsed = round(end - start, 3)
        print(f'Ended at: {elapsed} sec.')
        return result
    return wrapper

