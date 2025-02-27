import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api/v1"; // Replace with your backend URL

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add a request interceptor to include the auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// API methods
export const getDatasets = async (filter = "", limit = 10) => {
  try {
    const response = await api.get("/data", {
      params: { filter, limit },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching datasets:", error);
    throw error;
  }
};

export const createVisualization = async (dataset_id, chart_type) => {
  try {
    const response = await api.post("/visualizations", {
      dataset_id,
      chart_type,
    });
    return response.data;
  } catch (error) {
    console.error("Error creating visualization:", error);
    throw error;
  }
};

export default api;