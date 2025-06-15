from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.movies import router as movies_router
from api.search import router as search_router
from api.details import router as details_router
from api.genres import router as genres_router
from api.countries import router as countries_router
from api.recommendations import router as recommendations_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movies_router)
app.include_router(search_router)
app.include_router(details_router)
app.include_router(genres_router)
app.include_router(countries_router)
app.include_router(recommendations_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)