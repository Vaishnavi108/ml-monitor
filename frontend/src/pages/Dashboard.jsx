import { useState, useEffect } from "react";
import { getPredictions, getStats } from "../api/client";
import StatCard from "../components/StatCard";
import PredictionTable from "../components/PredictionTable";
import ConfidenceChart from "../components/ConfidenceChart";
import PredictionForm from "../components/PredictionForm";

export default function Dashboard() {
  const [predictions, setPredictions] = useState([]);
  const [stats, setStats] = useState(null);
  const [result, setResult] = useState(null);

  const fetchData = async () => {
    const [predsRes, statsRes] = await Promise.all([
      getPredictions(),
      getStats(),
    ]);
    setPredictions(predsRes.data);
    setStats(statsRes.data);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleResult = (data) => {
    setResult(data);
    fetchData(); // refresh table and stats
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">ML Model Monitor</h1>
          <p className="text-gray-500 text-sm mt-1">
            Income prediction model · v1.0.0
          </p>
        </div>

        {/* Stats */}
        {stats && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <StatCard
              title="Total Predictions"
              value={stats.total_predictions}
              color="blue"
            />
            <StatCard
              title="Avg Confidence"
              value={`${(stats.avg_confidence * 100).toFixed(1)}%`}
              color="green"
            />
            <StatCard
              title=">50K Rate"
              value={`${(stats.positive_rate * 100).toFixed(1)}%`}
              color="purple"
            />
            <StatCard
              title="Last 24h"
              value={stats.predictions_last_24h}
              color="amber"
            />
          </div>
        )}

        {/* Prediction result banner */}
        {result && (
          <div
            className={`mb-6 p-4 rounded-xl border text-sm font-medium ${
              result.prediction === 1
                ? "bg-green-50 border-green-200 text-green-700"
                : "bg-gray-50 border-gray-200 text-gray-600"
            }`}
          >
            Latest prediction: <strong>{result.label}</strong> with{" "}
            <strong>{(result.confidence * 100).toFixed(1)}%</strong> confidence
          </div>
        )}

        {/* Form + Chart */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <PredictionForm onResult={handleResult} />
          <ConfidenceChart predictions={predictions} />
        </div>

        {/* Table */}
        <PredictionTable predictions={predictions} />
      </div>
    </div>
  );
}
