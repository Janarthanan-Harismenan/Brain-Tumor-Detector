// src/api/api.js
import axios from "axios";

const API_URL = "http://localhost:8000"; // FastAPI backend URL

// Register user
export const signup = async (email, name, password) => {
  try {
    const response = await axios.post(`${API_URL}/signup`, { email, name, password });
    return response.data;
  } catch (error) {
    console.error(error);
    throw new Error("Error during signup");
  }
};

// Login user and get JWT token
export const login = async (email, password) => {
  try {
    const response = await axios.post(`${API_URL}/login`, new URLSearchParams({ username: email, password }));
    return response.data;
  } catch (error) {
    console.error(error);
    throw new Error("Error during login");
  }
};

// Upload image for prediction (without saving)
export const predictImage = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(`${API_URL}/predict`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      }
    });
    return response.data;
  } catch (error) {
    console.error(error);
    throw new Error("Error during prediction");
  }
};

// Upload image for prediction and save it to the database
export const uploadImageForPrediction = async (file, token) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(`${API_URL}/predict/save`, formData, {
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "multipart/form-data",
      }
    });
    return response.data;
  } catch (error) {
    console.error(error);
    throw new Error("Error during prediction");
  }
};

// Get saved predictions
export const getPredictions = async (token) => {
  try {
    const response = await axios.get(`${API_URL}/predictions`, {
      headers: {
        "Authorization": `Bearer ${token}`,
      }
    });
    return response.data;
  } catch (error) {
    console.error(error);
    throw new Error("Error fetching predictions");
  }
};
