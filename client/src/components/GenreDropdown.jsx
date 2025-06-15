import React from "react";

function GenreDropdown({ genres, onGenreSelect }) {
  return (
    <div className="relative group">
      <button className="text-white font-semibold px-4 py-2 rounded hover:bg-gray-700 transition-colors duration-200">
        Genres
      </button>
      <div className="absolute left-0 top-full z-20 hidden group-hover:block min-w-max bg-gray-800 shadow-lg rounded-md overflow-hidden">
        <div className="max-h-96 overflow-y-auto p-2">
          <div className="grid grid-cols-2 md:grid-cols-3 gap-x-6 gap-y-2">
            {genres.map((genre) => (
              <button
                key={genre.id}
                onClick={() => onGenreSelect(genre.id)}
                className="text-left py-2 px-3 text-sm text-white hover:bg-gray-700 hover:text-blue-400 rounded transition-colors duration-150 whitespace-nowrap"
              >
                {genre.name}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default GenreDropdown;