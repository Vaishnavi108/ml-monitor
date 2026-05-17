import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000/api/v1",
  headers: { "Content-Type": "application/json" },
});

export const getPredictions = () => API.get("/predictions/");
export const createPrediction = (data) => API.post("/predictions/", data);
export const getStats = () => API.get("/predictions/stats");
export const getHealth = () => API.get("/metrics/health");
