import { useState } from "react";

export default function StrategicInsightTool() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<{ answer: string; sources: string[] } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setResult(null);
    setError("");

    try {
      const response = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: query }),
      });

      if (!response.ok) throw new Error("Server error");

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Failed to fetch insights. Please try again.");
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div className="max-w-4xl mx-auto py-10 px-4 space-y-6">
      <h1 className="text-3xl font-bold text-gray-800"> Strategic Insight Generator</h1>
      
      <div className="flex gap-2">
        <input
          className="flex-1 px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:outline-none"
          placeholder="e.g., What can Deloitte help SFU with in 2025?"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Analyzing..." : "Get Insight"}
        </button>
      </div>

      {error && <p className="text-red-600">{error}</p>}

      {result && (
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6 space-y-6">
          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2"> Insight</h2>
            <p className="text-gray-700 whitespace-pre-wrap">{result.answer}</p>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Sources Referenced</h3>
            <ul className="list-disc list-inside text-sm text-gray-600 mt-1">
              {[...new Set(result.sources)].map((src, i) => (
                <li key={i}>{src}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
