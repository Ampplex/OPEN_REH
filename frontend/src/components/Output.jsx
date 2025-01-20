import React from "react";
import { useLocation, Link } from "react-router-dom";

const Output = () => {
  const location = useLocation();
  const { state } = location || {};
  const { response } = state || {};

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-4">Output Page</h1>
      {response ? (
        <div className="bg-gray-100 p-6 rounded-lg shadow-md">
          <h2 className="text-lg font-semibold">AI Agent Response:</h2>
          <p className="mt-4 text-gray-800">{response}</p>
        </div>
      ) : (
        <div className="bg-red-100 p-6 rounded-lg shadow-md">
          <h2 className="text-lg font-semibold text-red-600">
            No response available!
          </h2>
          <p className="mt-4 text-gray-800">
            Please go back and submit the form again.
          </p>
        </div>
      )}
      <Link
        to="/"
        className="mt-6 inline-block text-white bg-blue-500 px-4 py-2 rounded hover:bg-blue-600 transition"
      >
        Go Back
      </Link>
    </div>
  );
};

export default Output;