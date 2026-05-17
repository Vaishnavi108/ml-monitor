import { useState } from "react";
import { createPrediction } from "../api/client";

export default function PredictionForm({ onResult }) {
  const [form, setForm] = useState({
    age: 35,
    education_num: 13,
    hours_per_week: 40,
    capital_gain: 0,
    capital_diff: 0,
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: parseFloat(e.target.value) });
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await createPrediction(form);
      onResult(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fields = [
    { name: "age", label: "Age", min: 17, max: 90 },
    { name: "education_num", label: "Education Level (1-16)", min: 1, max: 16 },
    { name: "hours_per_week", label: "Hours per Week", min: 1, max: 99 },
    { name: "capital_gain", label: "Capital Gain", min: 0, max: 99999 },
    { name: "capital_diff", label: "Capital Diff", min: -99999, max: 99999 },
  ];

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <h2 className="text-sm font-semibold text-gray-600 mb-4">
        Make a Prediction
      </h2>
      <div className="grid grid-cols-2 gap-4">
        {fields.map((f) => (
          <div key={f.name}>
            <label className="text-xs text-gray-500 block mb-1">
              {f.label}
            </label>
            <input
              type="number"
              name={f.name}
              value={form[f.name]}
              onChange={handleChange}
              min={f.min}
              max={f.max}
              className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
          </div>
        ))}
      </div>
      <button
        onClick={handleSubmit}
        disabled={loading}
        className="mt-4 w-full bg-blue-600 text-white py-2 rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50 transition"
      >
        {loading ? "Predicting..." : "Run Prediction"}
      </button>
    </div>
  );
}
