# server/api/movies.py

from fastapi import APIRouter
from starlette.responses import JSONResponse
import time
from .config import TMDB_API_KEY, TMDB_BASE_URL, results_cache, cache_timeout, create_session

router = APIRouter()

@router.get("/movies/popular")
def get_popular_movies(page: int = 1):
    cache_key = f"popular_movies_page_{page}"
    if cache_key in results_cache:
        cached_data, timestamp = results_cache[cache_key]
        if time.time() - timestamp < cache_timeout:
            return cached_data
    
    try:
        session = create_session()
        response = session.get(
            f"{TMDB_BASE_URL}/movie/popular",
            params={
                "api_key": TMDB_API_KEY,
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
            content={"detail": f"Error fetching movies: {str(e)}"}
        )
    finally:
        if 'session' in locals():
            session.close()