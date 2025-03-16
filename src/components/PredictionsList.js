import { useEffect, useState } from "react";
import { getPredictions } from "../api/api";
import { useNavigate } from "react-router-dom";

function PredictionsList({ token, logout }) {
  const [predictions, setPredictions] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      navigate("/login"); // Redirect guests to login
      return;
    }

    const fetchPredictions = async () => {
      try {
        const data = await getPredictions(token);
        setPredictions(data);
      } catch (error) {
        alert("Error fetching predictions");
      }
    };

    fetchPredictions();
  }, [token, navigate]);

  return (
    <div>
      <h2>Your Predictions</h2>
      <button onClick={logout}>Logout</button> {/* Logout Button */}
      
      {/* Back Button */}
      <button onClick={() => navigate("/prediction")} style={{ marginLeft: "10px" }}>
        Back to Prediction
      </button>

      {predictions.length === 0 ? (
        <p>No saved predictions.</p>
      ) : (
        <ul>
          {predictions.map((prediction) => (
            <li key={prediction.id}>
              <img
                src={`data:image/png;base64,${prediction.image}`}
                alt="Prediction"
                width="100"
              />
              <p>Probability: {prediction.probability}</p>
              <p>Tumor Detected: {prediction.tumor_detected ? "Yes" : "No"}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default PredictionsList;
