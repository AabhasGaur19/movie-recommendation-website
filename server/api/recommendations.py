# # this is for recommendation directly from the TMDB page . no model used ... 
# # to use this uncomment the bottom code and also the code in client/MovieDetails.jsx
# # server/api/recommendations.py
# from fastapi import APIRouter
# from starlette.responses import JSONResponse
# import time
# from .config import TMDB_API_KEY, TMDB_BASE_URL, results_cache, cache_timeout, create_session

# router = APIRouter()

# @router.get("/recommend/{movie_id}")
# def get_movie_recommendations(movie_id: int, page: int = 1):
#     cache_key = f"recommendations_{movie_id}_page_{page}"
#     if cache_key in results_cache:
#         cached_data, timestamp = results_cache[cache_key]
#         if time.time() - timestamp < cache_timeout:
#             return cached_data
    
#     try:
#         session = create_session()
#         response = session.get(
#             f"{TMDB_BASE_URL}/movie/{movie_id}/recommendations",
#             params={
#                 "api_key": TMDB_API_KEY,
#                 "page": page,
#                 "language": "en-US"
#             },
#             timeout=30
#         )
        
#         response.raise_for_status()
#         data = response.json()
        
#         movies_list = data.get("results", [])
        
#         results_cache[cache_key] = (movies_list, time.time())
        
#         return movies_list
    
#     except Exception as e:
#         if cache_key in results_cache:
#             return results_cache[cache_key][0]
        
#         return JSONResponse(
#             status_code=503, 
#             content={"detail": f"Error fetching recommendations: {str(e)}"}
#         )
#     finally:
#         if 'session' in locals():
#             session.close()










# from fastapi import APIRouter, HTTPException
# from starlette.responses import JSONResponse
# import pickle
# import pandas as pd
# import numpy as np
# import time
# import os
# from .config import TMDB_API_KEY, TMDB_BASE_URL, results_cache, cache_timeout, create_session

# router = APIRouter()

# # Global variables to store the loaded model
# model_data = None
# model_loaded = False

# def load_recommendation_model():
#     """Load the movie recommendation model from pickle file"""
#     global model_data, model_loaded
    
#     if model_loaded and model_data is not None:
#         return model_data
    
#     try:
#         model_path = os.path.join("data", "movie_model.pkl")
        
#         if not os.path.exists(model_path):
#             raise FileNotFoundError(f"Model file not found at {model_path}")
        
#         with open(model_path, 'rb') as f:
#             model_data = pickle.load(f)
        
#         model_loaded = True
#         print(f"✅ Model loaded successfully from {model_path}")
#         return model_data
        
#     except Exception as e:
#         print(f"❌ Error loading model: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Failed to load recommendation model: {str(e)}")

# def get_movie_recommendations_from_model(tmdb_id: int, limit: int = 10):
#     """Get movie recommendations using the trained model"""
#     try:
#         model = load_recommendation_model()
#         df = model['df']
#         cosine_sim = model['cosine_sim']
        
#         # Find the movie by TMDB ID
#         movie_matches = df[df['id'] == tmdb_id]
        
#         if movie_matches.empty:
#             return None, "Movie not found in recommendation database"
        
#         movie_idx = movie_matches.index[0]
        
#         # Get similarity scores
#         sim_scores = list(enumerate(cosine_sim[movie_idx]))
#         sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
#         # Get top similar movies (excluding the movie itself)
#         movie_indices = [i[0] for i in sim_scores[1:limit+1]]
#         recommendations = df.iloc[movie_indices].copy()
        
#         # Extract TMDB IDs for the recommended movies
#         recommended_ids = recommendations['id'].tolist()
        
#         return recommended_ids, None
        
#     except Exception as e:
#         return None, f"Error generating recommendations: {str(e)}"

# def fetch_movie_details_from_tmdb(movie_id: int, max_retries: int = 3):
#     """Fetch movie details from TMDB API with retry logic"""
#     cache_key = f"movie_basic_{movie_id}"
    
#     # Check cache first
#     if cache_key in results_cache:
#         cached_data, timestamp = results_cache[cache_key]
#         if time.time() - timestamp < cache_timeout:
#             return cached_data
    
#     for attempt in range(max_retries):
#         session = None
#         try:
#             # Add delay between requests to avoid rate limiting
#             if attempt > 0:
#                 time.sleep(0.5 * attempt)  # Exponential backoff
            
#             session = create_session()
            
#             # Get basic movie details
#             movie_response = session.get(
#                 f"{TMDB_BASE_URL}/movie/{movie_id}",
#                 params={
#                     "api_key": TMDB_API_KEY,
#                     "language": "en-US"
#                 },
#                 timeout=15  # Reduced timeout
#             )
#             movie_response.raise_for_status()
#             movie_data = movie_response.json()
            
#             # Format the response according to frontend requirements
#             result = {
#                 "id": movie_data.get("id"),
#                 "title": movie_data.get("title"),
#                 "poster_path": movie_data.get("poster_path"),
#                 "overview": movie_data.get("overview"),
#                 "vote_average": movie_data.get("vote_average"),
#                 "release_date": movie_data.get("release_date")
#             }
            
#             # Cache the result
#             results_cache[cache_key] = (result, time.time())
            
#             return result
            
#         except Exception as e:
#             print(f"Attempt {attempt + 1} failed for movie {movie_id}: {str(e)}")
#             if attempt == max_retries - 1:  # Last attempt
#                 print(f"All attempts failed for movie {movie_id}")
#                 return None
#         finally:
#             if session:
#                 session.close()
                
#         # Small delay between retries
#         time.sleep(0.2)
    
#     return None

# @router.get("/recommend/{movie_id}")
# def get_movie_recommendations(movie_id: int):
#     """Get movie recommendations for a given movie ID"""
#     cache_key = f"recommendations_{movie_id}"
    
#     # Check cache first
#     if cache_key in results_cache:
#         cached_data, timestamp = results_cache[cache_key]
#         if time.time() - timestamp < cache_timeout:
#             return cached_data
    
#     try:
#         # Get recommended movie IDs from the model
#         recommended_ids, error = get_movie_recommendations_from_model(movie_id, limit=15)  # Get more to account for failures
        
#         if error:
#             return JSONResponse(
#                 status_code=404,
#                 content={"detail": error}
#             )
        
#         # Fetch details for each recommended movie from TMDB with rate limiting
#         recommendations = []
#         successful_fetches = 0
#         target_recommendations = 12
        
#         for i, rec_id in enumerate(recommended_ids):
#             if successful_fetches >= target_recommendations:
#                 break
                
#             # Add small delay between requests to avoid overwhelming TMDB
#             if i > 0:
#                 time.sleep(0.1)
            
#             movie_details = fetch_movie_details_from_tmdb(rec_id)
#             if movie_details:
#                 recommendations.append(movie_details)
#                 successful_fetches += 1
            
#             # If we're failing too much, stop trying
#             if i > 0 and successful_fetches == 0:
#                 break
        
#         if not recommendations:
#             return JSONResponse(
#                 status_code=404,
#                 content={"detail": "No recommendations could be fetched from TMDB"}
#             )
        
#         # Cache the results
#         results_cache[cache_key] = (recommendations, time.time())
        
#         print(f"✅ Successfully fetched {len(recommendations)} recommendations for movie {movie_id}")
#         return recommendations
        
#     except Exception as e:
#         # Try to return cached data if available
#         if cache_key in results_cache:
#             print(f"⚠️ Using cached data for movie {movie_id} due to error: {str(e)}")
#             return results_cache[cache_key][0]
        
#         return JSONResponse(
#             status_code=503,
#             content={"detail": f"Error generating recommendations: {str(e)}"}
#         )

# @router.get("/model/status")
# def get_model_status():
#     """Get the status of the recommendation model"""
#     try:
#         model = load_recommendation_model()
#         model_path = os.path.join("data", "movie_model.pkl")
#         file_size = os.path.getsize(model_path) / (1024 * 1024)  # Size in MB
        
#         return {
#             "status": "loaded",
#             "movies_count": len(model['df']),
#             "file_size_mb": round(file_size, 2),
#             "created_at": model.get('created_at', 'Unknown'),
#             "csv_source": model.get('csv_path', 'Unknown')
#         }
#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={
#                 "status": "error",
#                 "detail": f"Model not available: {str(e)}"
#             }
#         )










from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
import pickle
import pandas as pd
import numpy as np
import time
import os
import requests
from .config import TMDB_API_KEY, TMDB_BASE_URL, results_cache, cache_timeout, create_session
from .s3_utils import download_file_from_s3, get_s3_file_metadata, get_s3_client

router = APIRouter()

# Global variables to store the loaded model
model_data = None
model_loaded = False

def load_recommendation_model():
    """Load the movie recommendation model from AWS S3"""
    global model_data, model_loaded
    
    if model_loaded and model_data is not None:
        print("ℹ️ Using cached model from memory")
        return model_data
    
    start_time = time.time()
    try:
        # AWS S3 configuration
        s3_bucket = os.getenv("S3_BUCKET_NAME")
        s3_key = os.getenv("S3_MODEL_KEY", "movie_model.pkl")
        
        if not s3_bucket:
            raise ValueError("S3_BUCKET_NAME environment variable not set")
        
        # Verify S3 connectivity and file existence
        print(f"🔍 Verifying S3 access to {s3_key} in bucket {s3_bucket}")
        s3_client = get_s3_client()
        s3_client.head_object(Bucket=s3_bucket, Key=s3_key)
        print(f"✅ S3 access verified")
        
        # Download the model file from S3
        temp_file_path = download_file_from_s3(s3_bucket, s3_key)
        
        # Load the model from the downloaded file
        print(f"📂 Loading model from {temp_file_path}")
        try:
            with open(temp_file_path, 'rb') as f:
                model_data = pickle.load(f)
            print(f"✅ Model loaded in {time.time() - start_time:.2f} seconds")
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                print(f"✅ Cleaned up temporary file {temp_file_path}")
        
        model_loaded = True
        return model_data
        
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to load recommendation model: {str(e)}")

def get_movie_recommendations_from_model(tmdb_id: int, limit: int = 10):
    """Get movie recommendations using the trained model"""
    start_time = time.time()
    try:
        print(f"📈 Generating recommendations for movie ID {tmdb_id}")
        model = load_recommendation_model()
        df = model['df']
        cosine_sim = model['cosine_sim']
        
        # Find the movie by TMDB ID
        movie_matches = df[df['id'] == tmdb_id]
        
        if movie_matches.empty:
            print(f"⚠️ Movie ID {tmdb_id} not found in recommendation database")
            return None, "Movie not found in recommendation database"
        
        movie_idx = movie_matches.index[0]
        
        # Get similarity scores
        print("🔄 Computing similarity scores")
        sim_scores = list(enumerate(cosine_sim[movie_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top similar movies (excluding the movie itself)
        movie_indices = [i[0] for i in sim_scores[1:limit+1]]
        recommendations = df.iloc[movie_indices].copy()
        
        # Extract TMDB IDs for the recommended movies
        recommended_ids = recommendations['id'].tolist()
        print(f"✅ Generated {len(recommended_ids)} recommendations in {time.time() - start_time:.2f} seconds")
        
        return recommended_ids, None
        
    except Exception as e:
        print(f"❌ Error generating recommendations: {str(e)}")
        return None, f"Error generating recommendations: {str(e)}"

def fetch_movie_details_from_tmdb(movie_id: int, max_retries: int = 3):
    """Fetch movie details from TMDB API with retry logic"""
    cache_key = f"movie_basic_{movie_id}"
    
    # Check cache first
    if cache_key in results_cache:
        cached_data, timestamp = results_cache[cache_key]
        if time.time() - timestamp < cache_timeout:
            print(f"ℹ️ Using cached TMDB data for movie {movie_id}")
            return cached_data
    
    for attempt in range(max_retries):
        session = None
        try:
            # Add delay between requests to avoid rate limiting
            if attempt > 0:
                time.sleep(0.5 * attempt)  # Exponential backoff
            
            session = create_session()
            
            # Get basic movie details with timeout
            print(f"🌐 Fetching TMDB details for movie {movie_id}, attempt {attempt + 1}")
            movie_response = session.get(
                f"{TMDB_BASE_URL}/movie/{movie_id}",
                params={
                    "api_key": TMDB_API_KEY,
                    "language": "en-US"
                },
                timeout=15
            )
            movie_response.raise_for_status()
            movie_data = movie_response.json()
            
            # Format the response according to frontend requirements
            result = {
                "id": movie_data.get("id"),
                "title": movie_data.get("title"),
                "poster_path": movie_data.get("poster_path"),
                "overview": movie_data.get("overview"),
                "vote_average": movie_data.get("vote_average"),
                "release_date": movie_data.get("release_date")
            }
            
            # Cache the result
            results_cache[cache_key] = (result, time.time())
            print(f"✅ Fetched TMDB details for movie {movie_id}")
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Attempt {attempt + 1} failed for movie {movie_id}: {str(e)}")
            if attempt == max_retries - 1:
                print(f"❌ All attempts failed for movie {movie_id}")
                return None
        finally:
            if session:
                session.close()
                
        # Small delay between retries
        time.sleep(0.2)
    
    return None

@router.get("/recommend/{movie_id}")
def get_movie_recommendations(movie_id: int):
    """Get movie recommendations for a given movie ID"""
    cache_key = f"recommendations_{movie_id}"
    
    # Check cache first
    if cache_key in results_cache:
        cached_data, timestamp = results_cache[cache_key]
        if time.time() - timestamp < cache_timeout:
            print(f"ℹ️ Using cached recommendations for movie {movie_id}")
            return cached_data
    
    start_time = time.time()
    try:
        # Get recommended movie IDs from the model
        print(f"🚀 Starting recommendation process for movie {movie_id}")
        recommended_ids, error = get_movie_recommendations_from_model(movie_id, limit=15)
        
        if error:
            print(f"⚠️ Recommendation error: {error}")
            return JSONResponse(
                status_code=404,
                content={"detail": error}
            )
        
        # Fetch details for each recommended movie from TMDB
        recommendations = []
        successful_fetches = 0
        target_recommendations = 12
        
        for i, rec_id in enumerate(recommended_ids):
            if successful_fetches >= target_recommendations:
                break
                
            # Add delay to avoid TMDB rate limiting
            if i > 0:
                time.sleep(0.1)
            
            movie_details = fetch_movie_details_from_tmdb(rec_id)
            if movie_details:
                recommendations.append(movie_details)
                successful_fetches += 1
            else:
                print(f"⚠️ Failed to fetch details for recommended movie {rec_id}")
            
            # Stop if no successful fetches after first attempt
            if i > 0 and successful_fetches == 0:
                print("❌ No successful TMDB fetches, stopping")
                break
        
        if not recommendations:
            print("❌ No recommendations fetched from TMDB")
            return JSONResponse(
                status_code=404,
                content={"detail": "No recommendations could be fetched from TMDB"}
            )
        
        # Cache the results
        results_cache[cache_key] = (recommendations, time.time())
        print(f"✅ Successfully fetched {len(recommendations)} recommendations for movie {movie_id} in {time.time() - start_time:.2f} seconds")
        return recommendations
        
    except Exception as e:
        print(f"❌ Error in recommendation endpoint: {str(e)}")
        # Try to return cached data if available
        if cache_key in results_cache:
            print(f"⚠️ Using cached data for movie {movie_id} due to error: {str(e)}")
            return results_cache[cache_key][0]
        
        return JSONResponse(
            status_code=503,
            content={"detail": f"Error generating recommendations: {str(e)}"}
        )

@router.get("/model/status")
def get_model_status():
    """Get the status of the recommendation model"""
    try:
        start_time = time.time()
        model = load_recommendation_model()
        s3_bucket = os.getenv("S3_BUCKET_NAME")
        s3_key = os.getenv("S3_MODEL_KEY", "movie_model.pkl")
        
        # Get S3 object metadata for file size
        print("🔍 Fetching S3 metadata")
        metadata = get_s3_file_metadata(s3_bucket, s3_key)
        file_size = metadata['ContentLength'] / (1024 * 1024)  # Size in MB
        
        print(f"✅ Model status retrieved in {time.time() - start_time:.2f} seconds")
        return {
            "status": "loaded",
            "movies_count": len(model['df']),
            "file_size_mb": round(file_size, 2),
            "created_at": model.get('created_at', 'Unknown'),
            "source": f"s3://{s3_bucket}/{s3_key}"
        }
    except Exception as e:
        print(f"❌ Error fetching model status: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "detail": f"Model not available: {str(e)}"
            }
        )