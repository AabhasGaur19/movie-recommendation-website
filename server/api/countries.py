# server/api/countries.py

from fastapi import APIRouter
from starlette.responses import JSONResponse
import time
from .config import TMDB_API_KEY, TMDB_BASE_URL, results_cache, cache_timeout, create_session

router = APIRouter()

@router.get("/countries")
def get_movies_by_country(country_code: str, page: int = 1):
    cache_key = f"movies_country_{country_code.lower()}_page_{page}"
    if cache_key in results_cache:
        cached_data, timestamp = results_cache[cache_key]
        if time.time() - timestamp < cache_timeout:
            return cached_data
    
    try:
        session = create_session()
        response = session.get(
            f"{TMDB_BASE_URL}/discover/movie",
            params={
                "api_key": TMDB_API_KEY,
                "with_origin_country": country_code,
                "page": page,
                "language": "en-US"
            },
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json()
        
        movies_list = data.get("results", [])
        
        results_cache[cache_key] = (movies_list, time.time())
        
        return movies_list
    
    except Exception as e:
        if cache_key in results_cache:
            return results_cache[cache_key][0]
        
        return JSONResponse(
            status_code=503, 
            content={"detail": f"Error fetching country movies: {str(e)}"}
        )
    finally:
        if 'session' in locals():
            session.close()

@router.get("/country/list")
def get_country_list():
    countries = [
        {"code": "US", "name": "United States"},
        {"code": "IN", "name": "India"},
        {"code": "GB", "name": "United Kingdom"},
        {"code": "FR", "name": "France"},
        {"code": "JP", "name": "Japan"},
        {"code": "KR", "name": "South Korea"},
        {"code": "CA", "name": "Canada"},
        {"code": "AU", "name": "Australia"},
        {"code": "DE", "name": "Germany"},
        {"code": "IT", "name": "Italy"},
        {"code": "ES", "name": "Spain"},
        {"code": "CN", "name": "China"}
    ]
    return countries