# server/api/search.py

from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
import time
from .config import TMDB_API_KEY, TMDB_BASE_URL, results_cache, cache_timeout, create_session

router = APIRouter()

@router.get("/search")
def search_movies(query: str, page: int = 1):
    if not query or query.strip() == "":
        raise HTTPException(status_code=400, detail="Query parameter cannot be empty")
    
    cache_key = f"search_movies_{query.lower()}_page_{page}"
    if cache_key in results_cache:
        cached_data, timestamp = results_cache[cache_key]
        if time.time() - timestamp < cache_timeout:
            return cached_data
    
    try:
        session = create_session()
        response = session.get(
            f"{TMDB_BASE_URL}/search/movie",
            params={
                "api_key": TMDB_API_KEY,
                "query": query,
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
            content={"detail": f"Error searching movies: {str(e)}"}
        )
    finally:
        if 'session' in locals():
            session.close()