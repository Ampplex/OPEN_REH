import React, { useState, useEffect } from "react";
import { NavLink } from "react-router-dom";

const Interface = () => {
  const [exampleQuestion, setExampleQuestion] = useState("");
  const [darkMode, setDarkMode] = useState(false);
  const [parameters, setParameters] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (darkMode) {
      document.body.classList.add('dark');
    } else {
      document.body.classList.remove('dark');
    }
  }, [darkMode]);

  const handleFindBestAgent = async () => {
    setLoading(true); // Start loading state
    try {
      const response = await fetch("http://localhost:5050/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({
          prompt: exampleQuestion,
          param: parameters
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log("Success:", result);

      if (result.response) {
        console.log("Selected agent:", result.response);
        setResponse(result.response);
      }
    } catch (error) {
      console.error("Error:", error.message);
      setResponse("An error occurred. Please try again.");
    } finally {
      setLoading(false); // Stop loading state
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Example Question:", exampleQuestion);
    console.log("Parameters:", parameters);
    handleFindBestAgent();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-gray-900 dark:to-gray-800 transition-colors duration-200">
      {/* Top Navigation Bar */}
      <nav className="bg-gradient-to-r from-primary-600 to-secondary-600 dark:from-primary-800 dark:to-secondary-800 p-4 shadow-lg">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            open<span className="text-primary-200">REH</span>
          </h1>

          {/* Dark Mode Toggle */}
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="p-2.5 rounded-full bg-white/10 text-white hover:bg-white/20 transition-all duration-200 backdrop-blur-sm"
          >
            {darkMode ? (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
                className="w-5 h-5"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z"
                />
              </svg>
            ) : (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
                className="w-5 h-5"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z"
                />
              </svg>
            )}
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-3xl mx-auto">
          <div className="bg-white/70 dark:bg-gray-800/50 backdrop-blur-lg rounded-2xl p-8 shadow-xl">
            <h2 className="text-2xl font-bold mb-8 text-gray-800 dark:text-white text-center">
              AI Agent Selection Interface
            </h2>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Example Question Box */}
              <div className="space-y-2">
                <label
                  htmlFor="example-question"
                  className="block text-lg font-medium text-gray-700 dark:text-gray-200"
                >
                  Example Question
                </label>
                <textarea
                  id="example-question"
                  value={exampleQuestion}
                  onChange={(e) => setExampleQuestion(e.target.value)}
                  placeholder="Enter an example question you want the AI agent to answer..."
                  className="w-full h-32 p-4 border border-gray-200 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-300 transition-all duration-200"
                />
              </div>

              {/* Parameters Input */}
              <div className="space-y-2">
                <label
                  htmlFor="parameters"
                  className="block text-lg font-medium text-gray-700 dark:text-gray-200"
                >
                  Parameters
                </label>
                <textarea
                  id="parameters"
                  value={parameters}
                  onChange={(e) => setParameters(e.target.value)}
                  placeholder="Enter parameters (e.g., cost-effective, time-efficient)..."
                  className="w-full h-24 p-4 border border-gray-200 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-300 transition-all duration-200"
                />
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                className="w-full bg-gradient-to-r from-primary-500 to-secondary-500 text-white py-4 px-6 rounded-xl hover:from-primary-600 hover:to-secondary-600 transition-all duration-200 font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
              >
                Find Best AI Agent
              </button>
            </form>

            {/* Display the Response */}
            {response && !loading && (
              <div className="mt-6 p-4 bg-gray-100 dark:bg-gray-700 rounded-xl text-gray-800 dark:text-white">
                <h3 className="font-semibold text-lg">Response:</h3>
                <p>{response}</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Loading Modal */}
      {loading && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50 z-50">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-xl flex items-center space-x-4">
            <div className="animate-spin w-12 h-12 border-4 border-t-4 border-gray-600 dark:border-gray-300 rounded-full"></div>
            <span className="text-lg text-gray-800 dark:text-white">Loading...</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default Interface;