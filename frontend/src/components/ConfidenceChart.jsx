import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

export default function ConfidenceChart({ predictions }) {
  const buckets = [
    { range: "50-60%", min: 0.5, max: 0.6, count: 0 },
    { range: "60-70%", min: 0.6, max: 0.7, count: 0 },
    { range: "70-80%", min: 0.7, max: 0.8, count: 0 },
    { range: "80-90%", min: 0.8, max: 0.9, count: 0 },
    { range: "90-100%", min: 0.9, max: 1.01, count: 0 },
  ];

  predictions.forEach((p) => {
    const bucket = buckets.find(
      (b) => p.confidence >= b.min && p.confidence < b.max,
    );
    if (bucket) bucket.count++;
  });

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <h2 className="text-sm font-semibold text-gray-600 mb-4">
        Confidence Distribution
      </h2>
      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={buckets}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="range" tick={{ fontSize: 11 }} />
          <YAxis allowDecimals={false} tick={{ fontSize: 11 }} />
          <Tooltip />
          <Bar dataKey="count" radius={[4, 4, 0, 0]}>
            {buckets.map((_, i) => (
              <Cell
                key={i}
                fill={`hsl(${210 + i * 15}, 70%, ${55 + i * 5}%)`}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
