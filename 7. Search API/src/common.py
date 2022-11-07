import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

ELASTIC_SEARCH_API_ENDPOINT = os.getenv('ELASTIC_SEARCH_API_ENDPOINT', 'http://localhost:9200')