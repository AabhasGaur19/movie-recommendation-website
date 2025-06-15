import React, { useState, useEffect } from "react";
import axios from "axios";
import { Routes, Route } from "react-router-dom";
import MovieCard from "./components/MovieCard";
import MovieDetails from "./components/MovieDetails";
import Navbar from "./components/Navbar";

function Home() {
  const [movies, setMovies] = useState([]);
  const [genres, setGenres] = useState([]);
  const [countries, setCountries] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isSearching, setIsSearching] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedGenre, setSelectedGenre] = useState(null);
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [page, setPage] = useState(1);

  const fetchGenres = async () => {
    try {
      const response = await axios.get("http://localhost:8000/genre/list");
      setGenres(response.data);
    } catch (err) {
      console.error("Failed to fetch genres:", err);
    }
  };

  const fetchCountries = async () => {
    try {
      const response = await axios.get("http://localhost:8000/country/list");
      setCountries(response.data);
    } catch (err) {
      console.error("Failed to fetch countries:", err);
    }
  };

  const fetchMovies = async (endpoint, params = {}, append = false) => {
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:8000${endpoint}`, {
        params: { ...params, page },
      });
      setMovies((prevMovies) =>
        append ? [...prevMovies, ...response.data] : response.data
      );
      setError(null);
    } catch (err) {
      setError("Failed to fetch movies. Please try again later.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGenres();
    fetchCountries();
  }, []);
  
  useEffect(() => {
  if (isSearching && searchQuery.trim() === "") {
    clearSearch();
  }
}, [searchQuery]);


  useEffect(() => {
    setMovies([]); // Reset movies when filters change
    setPage(1); // Reset page
    if (isSearching && searchQuery) {
      fetchMovies("/search", { query: searchQuery });
    } else if (selectedCountry) {
      fetchMovies("/countries", { country_code: selectedCountry });
    } else if (selectedGenre) {
      fetchMovies("/genres", { genre_id: selectedGenre });
    } else {
      fetchMovies("/movies/popular");
    }
  }, [isSearching, searchQuery, selectedGenre, selectedCountry]);

  const handleLoadMore = () => {
    setPage((prevPage) => prevPage + 1);
    if (isSearching && searchQuery) {
      fetchMovies("/search", { query: searchQuery }, true);
    } else if (selectedCountry) {
      fetchMovies("/countries", { country_code: selectedCountry }, true);
    } else if (selectedGenre) {
      fetchMovies("/genres", { genre_id: selectedGenre }, true);
    } else {
      fetchMovies("/movies/popular", {}, true);
    }
  };

  const handleSearch = (query) => {
    setSearchQuery(query);
    setIsSearching(true);
    setSelectedGenre(null);
    setSelectedCountry(null);
    setPage(1);
    setMovies([]);
  };

  const clearSearch = () => {
    setSearchQuery("");
    setIsSearching(false);
    setPage(1);
    setMovies([]);
  };

  const handleGenreSelect = (genreId) => {
    setSelectedGenre(genreId);
    setSearchQuery("");
    setIsSearching(false);
    setSelectedCountry(null);
    setPage(1);
    setMovies([]);
  };

  const handleCountrySelect = (countryCode) => {
    setSelectedCountry(countryCode);
    setSearchQuery("");
    setIsSearching(false);
    setSelectedGenre(null);
    setPage(1);
    setMovies([]);
  };

  return (
    <div className="min-h-screen bg-black text-white font-sans">
      <Navbar
        genres={genres}
        countries={countries}
        onGenreSelect={handleGenreSelect}
        onCountrySelect={handleCountrySelect}
        onSearch={handleSearch}
      />

      <main className="container mx-auto px-4 py-10">
        {error && <div className="text-red-400 text-center mb-6">{error}</div>}

        {loading && movies.length === 0 ? (
          <div className="text-center text-gray-400 text-lg mt-10">
            <svg
              className="animate-spin h-10 w-10 text-blue-500 mx-auto mb-4"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            <p>Loading movies...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
            {movies.length === 0 ? (
              <p className="text-center text-gray-400 col-span-full">
                {isSearching
                  ? `No movies found for "${searchQuery}"`
                  : selectedCountry
                  ? "No movies found for this country"
                  : selectedGenre
                  ? "No movies found for this genre"
                  : "No movies available"}
              </p>
            ) : (
              movies.map((movie) => (
                <MovieCard
                  key={movie.id}
                  id={movie.id}
                  title={movie.title}
                  posterPath={movie.poster_path}
                  overview={movie.overview}
                  rating={movie.vote_average}
                  releaseDate={movie.release_date}
                />
              ))
            )}
          </div>
        )}

        {movies.length > 0 && !loading && (
          <div className="text-center mt-8">
            <button
              onClick={handleLoadMore}
              className="px-6 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition duration-300"
            >
              Load More
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/movie/:id" element={<MovieDetails />} />
    </Routes>
  );
}

export default App;
