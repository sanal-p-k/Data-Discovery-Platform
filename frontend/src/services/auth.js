import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api/v1"; // Replace with your backend URL

// Login user and store token
export const login = async (username, password) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth/token`, {
      username,
      password,
    });
    const { access_token } = response.data;
    localStorage.setItem("access_token", access_token);
    return access_token;
  } catch (error) {
    console.error("Error logging in:", error);
    throw error;
  }
};

// Logout user and remove token
export const logout = () => {
  localStorage.removeItem("access_token");
};

// Get the current user's details
export const getCurrentUser = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/auth/me`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching current user:", error);
    throw error;
  }
};

// Check if the user is authenticated
export const isAuthenticated = () => {
  return !!localStorage.getItem("access_token");
};