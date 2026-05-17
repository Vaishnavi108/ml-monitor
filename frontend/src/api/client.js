import axios from "axios";

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000/api/v1",
  headers: { "Content-Type": "application/json" },
});

export const getPredictions = () => API.get("/predictions/");
export const createPrediction = (data) => API.post("/predictions/", data);
export const getStats = () => API.get("/predictions/stats");
export const getHealth = () => API.get("/metrics/health");
