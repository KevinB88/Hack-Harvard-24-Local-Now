// import React from 'react';
import { FaSearch } from "react-icons/fa";

export default function Searchbar() {
  return (
    <div className="flex justify-center mb-10 ">
      <form>
        {/* Icon inside the search input */}
        <div className="relative">
        <span className="absolute w-12 h-12 bg-blue-400 rounded-full -z-1"></span>
          <FaSearch className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-800 text-xl" />
          
          <input
            type="Search"
            placeholder="Search..."
            className="h-12 pl-12 pr-4 rounded-full bg-gray-300 text-black placeholder-gray-500"
            
          />
          
        </div>
      </form>
    </div>
  );
}
