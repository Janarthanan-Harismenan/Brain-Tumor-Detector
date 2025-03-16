import { useNavigate } from "react-router-dom";

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="h-screen flex flex-col">
      {/* Navigation Bar */}
      <nav className="bg-gray-900 text-white py-4 px-6 shadow-lg">
        <h1 className="text-2xl font-bold text-center">Brain Tumor Detector</h1>
      </nav>

      {/* Main Content */}
      <div className="flex flex-1 flex-col items-center justify-center bg-gray-100">
        <h2 className="text-3xl font-semibold mb-6 text-gray-800">
          Welcome to Brain Tumor Detector
        </h2>
        <p className="text-gray-600 mb-8 text-center max-w-lg">
          Detect brain tumors with AI-powered image analysis. Login or continue as a guest to proceed.
        </p>

        {/* Buttons */}
        <div className="space-x-4">
          <button
            onClick={() => navigate("/login")}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium shadow-md transition duration-300"
          >
            Login
          </button>

          <button
            onClick={() => navigate("/prediction")}
            className="bg-gray-700 hover:bg-gray-800 text-white px-6 py-3 rounded-lg font-medium shadow-md transition duration-300"
          >
            Continue as Guest
          </button>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
