// // this will give direct recommendation from the tmdb
// // to use this :: uncomment the server/recommendation.py code 
// import React, { useState, useEffect } from "react";
// import { useParams, Link } from "react-router-dom";
// import axios from "axios";
// import MovieCard from "./MovieCard";

// function MovieDetails() {
//   const { id } = useParams();
//   const [movie, setMovie] = useState(null);
//   const [recommendations, setRecommendations] = useState([]);
//   const [error, setError] = useState(null);
//   const [recError, setRecError] = useState(null);
//   const [loading, setLoading] = useState(true);
//   const [recLoading, setRecLoading] = useState(true);
//   const [recPage, setRecPage] = useState(1);

//   const fetchMovie = async () => {
//     try {
//       setLoading(true);
//       const response = await axios.get(`http://localhost:8000/movie/${id}`);
//       setMovie(response.data);
//       setError(null);
//     } catch (err) {
//       setError("Failed to fetch movie details. Please try again later.");
//       console.error(err);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const fetchRecommendations = async (page, append = false) => {
//     try {
//       setRecLoading(true);
//       const response = await axios.get(
//         `http://localhost:8000/recommend/${id}`,
//         {
//           params: { page },
//         }
//       );
//       setRecommendations((prev) =>
//         append ? [...prev, ...response.data] : response.data
//       );
//       setRecError(null);
//     } catch (err) {
//       setRecError("Failed to fetch recommendations.");
//       console.error(err);
//     } finally {
//       setRecLoading(false);
//     }
//   };

//   useEffect(() => {
//     fetchMovie();
//     fetchRecommendations(recPage);
//   }, [id]);

//   useEffect(() => {
//     if (recPage > 1) {
//       fetchRecommendations(recPage, true);
//     }
//   }, [recPage]);

//   const handleLoadMoreRecommendations = () => {
//     setRecPage((prevPage) => prevPage + 1);
//   };
//   if (error) {
//     return (
//       <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex items-center justify-center">
//         <div className="text-center">
//           <p className="text-red-400 mb-4">{error}</p>
//           <Link to="/" className="text-blue-400 hover:text-blue-300 underline">
//             Back to Home
//           </Link>
//         </div>
//       </div>
//     );
//   }

//   if (loading) {
//     return (
//       <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex items-center justify-center">
//         <div className="text-center text-gray-400 text-lg">
//           <svg
//             className="animate-spin h-8 w-8 mx-auto"
//             xmlns="http://www.w3.org/2000/svg"
//             fill="none"
//             viewBox="0 0 24 24"
//           >
//             <circle
//               className="opacity-25"
//               cx="12"
//               cy="12"
//               r="10"
//               stroke="currentColor"
//               strokeWidth="4"
//             ></circle>
//             <path
//               className="opacity-75"
//               fill="currentColor"
//               d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
//             ></path>
//           </svg>
//           Loading movie details...
//         </div>
//       </div>
//     );
//   }

//   const imageUrl = movie.poster_path
//     ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
//     : "https://t4.ftcdn.net/jpg/05/97/47/95/360_F_597479556_7bbQ7t4Z8k3xbAloHFHVdZIizWK1PdOo.jpg";

//   return (
//     <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white">
//       <header className="bg-gray-900 bg-opacity-75 py-6 shadow-md">
//         <div className="flex items-center justify-center relative">
//           {/* Back Arrow Button */}
//           <Link
//             to="/"
//             className="absolute left-4 text-blue-400 hover:text-blue-300 transition-colors duration-200 flex items-center"
//           >
//             <svg
//               className="w-6 h-6 mr-1"
//               fill="none"
//               stroke="currentColor"
//               strokeWidth="2"
//               viewBox="0 0 24 24"
//               xmlns="http://www.w3.org/2000/svg"
//             >
//               <path
//                 strokeLinecap="round"
//                 strokeLinejoin="round"
//                 d="M15 19l-7-7 7-7"
//               />
//             </svg>
//             <span className="hidden sm:inline">Back</span>
//           </Link>

//           {/* Title */}
//           <h1 className="text-4xl font-extrabold text-center tracking-wider">
//             Movie Details
//           </h1>
//         </div>
//       </header>

//       <main className="container mx-auto px-4 py-8">
//         <div className="flex flex-col md:flex-row gap-8">
//           <div className="md:w-1/3">
//             <img
//               src={imageUrl}
//               alt={`${movie.title} poster`}
//               className="w-full rounded-xl shadow-lg"
//             />
//           </div>
//           <div className="md:w-2/3">
//             <h2 className="text-3xl font-bold mb-4">{movie.title}</h2>
//             <p className="text-gray-400 mb-2">
//               <span className="text-yellow-400">⭐</span>{" "}
//               {movie.vote_average?.toFixed(1) || "N/A"} |{" "}
//               {movie.runtime ? `${movie.runtime} min` : "N/A"} |{" "}
//               {movie.release_date || "N/A"}
//             </p>
//             <p className="text-gray-300 mb-4">
//               {movie.overview || "No overview available"}
//             </p>
//             <p className="mb-2">
//               <span className="font-semibold">Director:</span>{" "}
//               {movie.director || "N/A"}
//             </p>
//             <p className="mb-2">
//               <span className="font-semibold">Cast:</span>{" "}
//               {movie.cast?.length > 0 ? movie.cast.join(", ") : "N/A"}
//             </p>
//             <p className="mb-2">
//               <span className="font-semibold">Genres:</span>{" "}
//               {movie.genres?.length > 0 ? movie.genres.join(", ") : "N/A"}
//             </p>
//           </div>
//         </div>

//         <section className="mt-12">
//           <h2 className="text-2xl font-bold mb-6">Recommended Movies</h2>
//           {recLoading && recommendations.length === 0 ? (
//             <div className="text-center text-gray-400 text-lg">
//               <svg
//                 className="animate-spin h-8 w-8 mx-auto"
//                 xmlns="http://www.w3.org/2000/svg"
//                 fill="none"
//                 viewBox="0 0 24 24"
//               >
//                 <circle
//                   className="opacity-25"
//                   cx="12"
//                   cy="12"
//                   r="10"
//                   stroke="currentColor"
//                   strokeWidth="4"
//                 ></circle>
//                 <path
//                   className="opacity-75"
//                   fill="currentColor"
//                   d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
//                 ></path>
//               </svg>
//               Loading recommendations...
//             </div>
//           ) : recError ? (
//             <p className="text-red-400 text-center">{recError}</p>
//           ) : recommendations.length === 0 ? (
//             <p className="text-gray-400 text-center">
//               No recommendations available
//             </p>
//           ) : (
//             <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
//               {recommendations.map((movie) => (
//                 <MovieCard
//                   key={movie.id}
//                   id={movie.id}
//                   title={movie.title}
//                   posterPath={movie.poster_path}
//                   overview={movie.overview}
//                   rating={movie.vote_average}
//                   releaseDate={movie.release_date}
//                 />
//               ))}
//             </div>
//           )}
//           {recommendations.length > 0 && !recLoading && (
//             <div className="text-center mt-8">
//               <button
//                 onClick={handleLoadMoreRecommendations}
//                 className="px-6 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition duration-300"
//               >
//                 Load More Recommendations
//               </button>
//             </div>
//           )}
//         </section>
//       </main>
//     </div>
//   );
// }

// export default MovieDetails;


import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import MovieCard from "./MovieCard";
import config from "../api/config";

function MovieDetails() {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState(null);
  const [recError, setRecError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [recLoading, setRecLoading] = useState(true);

  const fetchWithRetry = async (url, maxRetries = 3, delay = 2000) => {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        const response = await axios.get(url, { timeout: 30000 }); // 30s timeout
        return response;
      } catch (err) {
        if (err.response && err.response.status === 503 && attempt < maxRetries) {
          console.warn(`Attempt ${attempt} failed with 503. Retrying in ${delay}ms...`);
          await new Promise((resolve) => setTimeout(resolve, delay));
          continue;
        }
        throw err;
      }
    }
  };

  const fetchMovie = async () => {
    try {
      setLoading(true);
      const response = await fetchWithRetry(`${config.API_BASE_URL}/api/movie/${id}`);
      setMovie(response.data);
      setError(null);
    } catch (err) {
      setError("Failed to fetch movie details. Please try again later.");
      console.error("Fetch movie error:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchRecommendations = async () => {
    try {
      setRecLoading(true);
      const response = await fetchWithRetry(`${config.API_BASE_URL}/api/recommend/${id}`);
      setRecommendations(response.data);
      setRecError(null);
    } catch (err) {
      if (err.response && err.response.status === 404) {
        setRecError("No recommendations available for this movie.");
      } else {
        setRecError("Failed to fetch recommendations. Please try again later.");
      }
      console.error("Fetch recommendations error:", err);
    } finally {
      setRecLoading(false);
    }
  };

  useEffect(() => {
    fetchMovie();
    fetchRecommendations();
  }, [id]);

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-400 mb-4">{error}</p>
          <Link to="/" className="text-blue-400 hover:text-blue-300 underline">
            Back to Home
          </Link>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex items-center justify-center">
        <div className="text-center text-gray-400 text-lg">
          <svg
            className="animate-spin h-8 w-8 mx-auto"
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
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          Loading movie details...
        </div>
      </div>
    );
  }

  const imageUrl = movie.poster_path
    ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
    : "https://t4.ftcdn.net/jpg/05/97/47/95/360_F_597479556_7bbQ7t4Z8k3xbAloHFHVdZIizWK1PdOo.jpg";

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white">
      <header className="bg-gray-900 bg-opacity-75 py-6 shadow-md">
        <div className="flex items-center justify-center relative">
          <Link
            to="/"
            className="absolute left-4 text-blue-400 hover:text-blue-300 transition-colors duration-200 flex items-center"
          >
            <svg
              className="w-6 h-6 mr-1"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M15 19l-7-7 7-7"
              />
            </svg>
            <span className="hidden sm:inline">Back</span>
          </Link>
          <h1 className="text-4xl font-extrabold text-center tracking-wider">
            Movie Details
          </h1>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row gap-8">
          <div className="md:w-1/3">
            <img
              src={imageUrl}
              alt={`${movie.title} poster`}
              className="w-full rounded-xl shadow-lg"
            />
          </div>
          <div className="md:w-2/3">
            <h2 className="text-3xl font-bold mb-4">{movie.title}</h2>
            <p className="text-gray-400 mb-2">
              <span className="text-yellow-400">⭐</span>{" "}
              {movie.vote_average?.toFixed(1) || "N/A"} |{" "}
              {movie.runtime ? `${movie.runtime} min` : "N/A"} |{" "}
              {movie.release_date || "N/A"}
            </p>
            <p className="text-gray-300 mb-4">
              {movie.overview || "No overview available"}
            </p>
            <p className="mb-2">
              <span className="font-semibold">Director:</span>{" "}
              {movie.director || "N/A"}
            </p>
            <p className="mb-2">
              <span className="font-semibold">Cast:</span>{" "}
              {movie.cast?.length > 0 ? movie.cast.join(", ") : "N/A"}
            </p>
            <p className="mb-2">
              <span className="font-semibold">Genres:</span>{" "}
              {movie.genres?.length > 0 ? movie.genres.join(", ") : "N/A"}
            </p>
          </div>
        </div>

        <section className="mt-12">
          <h2 className="text-2xl font-bold mb-6">Recommended Movies</h2>
          {recLoading ? (
            <div className="text-center text-gray-400 text-lg">
              <svg
                className="animate-spin h-8 w-8 mx-auto"
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
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              Loading recommendations... (This may take a moment due to server startup)
            </div>
          ) : recError ? (
            <p className="text-red-400 text-center">{recError}</p>
          ) : recommendations.length === 0 ? (
            <p className="text-gray-400 text-center">
              No recommendations available
            </p>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
              {recommendations.map((movie) => (
                <MovieCard
                  key={movie.id}
                  id={movie.id}
                  title={movie.title}
                  posterPath={movie.poster_path}
                  rating={movie.vote_average}
                  releaseDate={movie.release_date}
                />
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default MovieDetails;