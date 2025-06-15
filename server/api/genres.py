# server/api/genres.py

from fastapi import APIRouter
from starlette.responses import JSONResponse
import time
from .config import TMDB_API_KEY, TMDB_BASE_URL, results_cache, cache_timeout, create_session

router = APIRouter()

@router.get("/genres")
def get_movies_by_genre(genre_id: int, page: int = 1):
    cache_key = f"movies_genre_{genre_id}_page_{page}"
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
                "with_genres": genre_id,
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
            content={"detail": f"Error fetching genre movies: {str(e)}"}
        )
    finally:
        if 'session' in locals():
            session.close()

@router.get("/genre/list")
def get_genre_list():
    cache_key = "genre_list"
    if cache_key in results_cache:
        cached_data, timestamp = results_cache[cache_key]
        if time.time() - timestamp < cache_timeout:
            return cached_data
    
    try:
        session = create_session()
        response = session.get(
            f"{TMDB_BASE_URL}/genre/movie/list",
            params={
                "api_key": TMDB_API_KEY,
                "language": "en-US"
            },
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json()
        
        genres = data.get("genres", [])
        
        results_cache[cache_key] = (genres, time.time())
        
        return genres
    
    except Exception as e:
        if cache_key in results_cache:
            return results_cache[cache_key][0]
        
        return JSONResponse(
            status_code=503, 
            content={"detail": f"Error fetching genre list: {str(e)}"}
        )
    finally:
        if 'session' in locals():
            session.close()