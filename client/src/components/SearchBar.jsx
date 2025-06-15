import React, { useState, useEffect } from "react";

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState("");

  useEffect(() => {
    const debounce = setTimeout(() => {
      onSearch(query);
    }, 300);

    return () => clearTimeout(debounce);
  }, [query]);

  const handleChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault(); 
    onSearch(query); 
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex items-center bg-gray-900 border border-gray-700 rounded-full overflow-hidden"
    >
      <input
        type="text"
        value={query}
        onChange={handleChange}
        placeholder="Search for a movie..."
        className="flex-grow px-3 py-2 bg-transparent text-white placeholder-gray-400 focus:outline-none"
      />
      <button
        type="submit"
        className="px-5 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-500 hover:to-purple-500 transition-colors duration-300"
      >
        Search
      </button>
    </form>
  );
}

export default SearchBar;
