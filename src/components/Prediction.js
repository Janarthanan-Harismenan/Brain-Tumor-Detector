import { useState } from "react";
import { uploadImageForPrediction, predictImage } from "../api/api";
import { useNavigate } from "react-router-dom";

function Prediction({ token, logout }) {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) {
      alert("Please select an image to upload.");
      return;
    }

    setLoading(true);
    setResult(null); // Clear previous results

    try {
      let data;
      if (token) {
        data = await uploadImageForPrediction(image, token);
      } else {
        data = await predictImage(image); 
      }

      console.log("Prediction result:", data.result);
      setResult(data.result); // Set the result from the API response

      if (token) {
        alert("Prediction saved successfully!");
      } else {
        alert("Prediction complete! Login to save results.");
      }
    } catch (error) {
      alert("Error during prediction");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <div className="bg-white shadow-lg rounded-lg p-6 max-w-md w-full">
        {/* Header */}
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold text-center flex-1">Upload Image for Prediction</h2>

          {/* Show logout button if user is logged in */}
          {token && (
            <button
              onClick={logout} // Now uses the logout function from App.js
              className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition"
            >
              Logout
            </button>
          )}
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col space-y-4 mt-4">
          <input
            type="file"
            onChange={handleImageChange}
            className="border p-2 rounded w-full"
          />
          <button
            type="submit"
            className="bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition"
            disabled={loading}
          >
            {loading ? "Processing..." : "Predict"}
          </button>
        </form>

        {/* Show Prediction Result if available */}
        {result && (
          <div className="mt-6 bg-gray-200 p-4 rounded text-center">
            <h3 className="text-lg font-semibold">Prediction Result</h3>
            <p><strong>Probability:</strong> {result.probability}</p>
            <p><strong>Tumor Detected:</strong> {result.tumor_detected ? "Yes" : "No"}</p>
            <img
              src={`data:image/png;base64,${result.image}`}
              alt="Prediction Result"
              className="mt-4 rounded-lg shadow-md w-full"
            />
          </div>
        )}

        {/* Show "View History" button only if user is authenticated */}
        {token && (
          <button
            onClick={() => navigate("/predictions-list")}
            className="mt-4 w-full bg-green-500 text-white py-2 rounded hover:bg-green-600 transition"
          >
            View History
          </button>
        )}
      </div>
    </div>
  );
}

export default Prediction;
