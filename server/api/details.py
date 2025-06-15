# server/api/details.py

from fastapi import APIRouter
from starlette.responses import JSONResponse
import time
from .config import TMDB_API_KEY, TMDB_BASE_URL, results_cache, cache_timeout, create_session

router = APIRouter()

@router.get("/movie/{movie_id}")
def get_movie_details(movie_id: int):
    cache_key = f"movie_details_{movie_id}"
    if cache_key in results_cache:
        cached_data, timestamp = results_cache[cache_key]
        if time.time() - timestamp < cache_timeout:
            return cached_data
    
    try:
        session = create_session()
        movie_response = session.get(
            f"{TMDB_BASE_URL}/movie/{movie_id}",
            params={
                "api_key": TMDB_API_KEY,
                "language": "en-US"
            },
            timeout=30
        )
        movie_response.raise_for_status()
        movie_data = movie_response.json()
        
        credits_response = session.get(
            f"{TMDB_BASE_URL}/movie/{movie_id}/credits",
            params={
                "api_key": TMDB_API_KEY,
                "language": "en-US"
            },
            timeout=30
        )
        credits_response.raise_for_status()
        credits_data = credits_response.json()
        
        director = next(
            (crew["name"] for crew in credits_data.get("crew", []) if crew["job"] == "Director"),
            "Unknown"
        )
        
        cast = [actor["name"] for actor in credits_data.get("cast", [])[:5]]
        
        result = {
            "id": movie_data.get("id"),
            "title": movie_data.get("title"),
            "overview": movie_data.get("overview"),
            "poster_path": movie_data.get("poster_path"),
            "release_date": movie_data.get("release_date"),
            "vote_average": movie_data.get("vote_average"),
            "runtime": movie_data.get("runtime"),
            "genres": [genre["name"] for genre in movie_data.get("genres", [])],
            "director": director,
            "cast": cast
        }
        
        results_cache[cache_key] = (result, time.time())
        
        return result
    
    except Exception as e:
        if cache_key in results_cache:
            return results_cache[cache_key][0]
        
        return JSONResponse(
            status_code=503, 
            content={"detail": f"Error fetching movie details: {str(e)}"}
        )
    finally:
        if 'session' in locals():
            session.close()