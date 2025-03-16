import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useState } from "react";
import HomePage from "./components/HomePage";
import Login from "./components/Login";
import Prediction from "./components/Prediction";
import PredictionsList from "./components/PredictionsList";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");

  const saveToken = (userToken) => {
    localStorage.setItem("token", userToken);
    setToken(userToken);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken("");
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login setToken={saveToken} />} />
        <Route path="/prediction" element={<Prediction token={token} setToken={saveToken} logout={logout} />} />
        <Route
          path="/predictions-list"
          element={token ? <PredictionsList token={token} logout={logout} /> : <Navigate to="/login" />}
        />
      </Routes>
    </Router>
  );
}

export default App;
