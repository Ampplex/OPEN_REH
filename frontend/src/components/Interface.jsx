import React, { useState, useEffect } from "react";

const Interface = () => {
  const [exampleQuestion, setExampleQuestion] = useState("");
  const [darkMode, setDarkMode] = useState(false);
  const [parameters, setParameters] = useState("");

  const handleFindBestAgent = () => {
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
  
    const data = {
      prompt: exampleQuestion,  // Use the actual form value
      param: parameters        // Use the actual form value
    };
  
    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: JSON.stringify(data),
      credentials: 'omit'  // Don't send cookies
    };
  
    fetch("http://localhost:5050/submit", requestOptions)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(result => {
        console.log("Success:", result);
        // Handle successful response here
      })
      .catch(error => {
        console.error("Error:", error);
        // Handle error here
      });
  };

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [darkMode]);

  const handleSubmit = (e) => {
    e.preventDefault();

    // Convert parameters string to array by splitting on commas and trimming whitespace
    const parameterArray = parameters
      .split(",")
      .map((param) => param.trim())
      .filter((param) => param !== "");
    handleFindBestAgent()
    console.log("Example Question:", exampleQuestion);
    console.log("Parameters:", parameterArray);
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
          </div>
        </div>
      </div>
    </div>
  );
};

export default Interface;
