import React from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";

function MovieCard({ id, title, posterPath, overview, rating, releaseDate }) {
  const imageUrl = posterPath
    ? `https://image.tmdb.org/t/p/w500${posterPath}`
    : "https://t4.ftcdn.net/jpg/05/97/47/95/360_F_597479556_7bbQ7t4Z8k3xbAloHFHVdZIizWK1PdOo.jpg";

  return (
    <Link to={`/movie/${id}`} className="block">
      <div className="relative rounded-xl overflow-hidden shadow-lg group transform transition-transform duration-300 hover:scale-105">
        <img
          src={imageUrl}
          alt={`${title} poster`}
          className="w-full h-full object-cover transition duration-500 group-hover:blur-sm"
        />
        <div className="absolute bottom-0 left-0 right-0 bg-opacity-60 text-white p-4 transform translate-y-full group-hover:translate-y-0 transition-transform duration-500 ease-in-out">
          <h3 className="text-lg font-semibold mb-1">{title}</h3>
          <div className="text-sm text-yellow-400 mb-1">
            ⭐ {rating ? rating.toFixed(1) : "N/A"} 📅 {releaseDate || "N/A"}
          </div>
          <p className="text-sm line-clamp-4">
            {overview || "No overview available"}
          </p>
        </div>
      </div>
    </Link>
  );
}

MovieCard.propTypes = {
  id: PropTypes.number.isRequired,
  title: PropTypes.string.isRequired,
  posterPath: PropTypes.string,
  overview: PropTypes.string,
  rating: PropTypes.number,
  releaseDate: PropTypes.string,
};

MovieCard.defaultProps = {
  posterPath: null,
  overview: "",
  rating: null,
  releaseDate: "",
};

export default MovieCard;
