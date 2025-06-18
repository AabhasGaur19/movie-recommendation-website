import React, { useState, useEffect } from "react";

function CountryDropdown({ countries, onCountrySelect }) {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (!e.target.closest(".dropdown-container")) {
        setIsOpen(false);
      }
    };
    document.addEventListener("click", handleClickOutside);
    return () => document.removeEventListener("click", handleClickOutside);
  }, []);

  return (
    <div
      className="relative dropdown-container group"
      onMouseEnter={() => setIsOpen(true)}
      onMouseLeave={() => setIsOpen(false)}
    >
      <button
        type="button"
        onClick={() => setIsOpen((prev) => !prev)} // Toggle on mobile
        className="text-white font-semibold px-4 py-2 rounded hover:bg-gray-700 transition-colors duration-200"
      >
        Countries
      </button>

      <div
        className={`absolute left-0 top-full z-20 min-w-max bg-gray-800 shadow-lg rounded-md overflow-hidden ${
          isOpen ? "block" : "hidden"
        }`}
      >
        <div className="max-h-96 overflow-y-auto p-2">
          <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 gap-x-4 gap-y-2">
            {countries.map((country) => (
              <button
                key={country.code}
                onClick={() => {
                  onCountrySelect(country.code);
                  setIsOpen(false); 
                }}
                className="text-left py-2 px-3 text-sm text-white hover:bg-gray-700 hover:text-blue-400 rounded transition-colors duration-150 whitespace-nowrap"
              >
                {country.name}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default CountryDropdown;