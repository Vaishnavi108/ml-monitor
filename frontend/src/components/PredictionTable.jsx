export default function PredictionTable({ predictions }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <div className="px-5 py-4 border-b border-gray-100">
        <h2 className="text-sm font-semibold text-gray-600">
          Recent Predictions
        </h2>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 text-gray-500 text-xs uppercase">
            <tr>
              <th className="px-4 py-3 text-left">ID</th>
              <th className="px-4 py-3 text-left">Label</th>
              <th className="px-4 py-3 text-left">Confidence</th>
              <th className="px-4 py-3 text-left">Time</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {predictions.map((p) => (
              <tr key={p.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-gray-400">#{p.id}</td>
                <td className="px-4 py-3">
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${
                      p.prediction === 1
                        ? "bg-green-100 text-green-700"
                        : "bg-gray-100 text-gray-600"
                    }`}
                  >
                    {p.label}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <div className="w-20 bg-gray-100 rounded-full h-1.5">
                      <div
                        className="bg-blue-500 h-1.5 rounded-full"
                        style={{ width: `${p.confidence * 100}%` }}
                      />
                    </div>
                    <span className="text-gray-500">
                      {(p.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                </td>
                <td className="px-4 py-3 text-gray-400">
                  {new Date(p.created_at).toLocaleTimeString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {predictions.length === 0 && (
          <p className="text-center text-gray-400 py-8">No predictions yet</p>
        )}
      </div>
    </div>
  );
}
