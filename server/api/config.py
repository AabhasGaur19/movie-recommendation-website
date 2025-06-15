# server/api/config.py
import requests
from requests.adapters import HTTPAdapter, Retry
import time

TMDB_API_KEY = "085fb95ff095c18b3656683bf65e5311"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

results_cache = {}
cache_timeout = 300

def create_session():
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session