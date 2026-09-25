import { useEffect, useState } from "react";
import { getVideos, toggleFavorite, logWatch } from "../services/videos";
import Card from "../components/Card";
import { Spinner, EmptyState, ErrorState } from "../components/StateComponents";

const CATEGORIES = [
  { value: "", label: "All categories" },
  { value: "crop_farming", label: "Crop farming" },
  { value: "organic_farming", label: "Organic farming" },
  { value: "fertilizers", label: "Fertilizers" },
  { value: "irrigation", label: "Irrigation" },
  { value: "pest_management", label: "Pest management" },
  { value: "modern_farming", label: "Modern farming" },
  { value: "government_schemes", label: "Government schemes" },
  { value: "machinery", label: "Machinery" },
  { value: "soil_management", label: "Soil management" },
];

export default function Videos() {
  const [videos, setVideos] = useState([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  function load() {
    setLoading(true);
    setError("");
    getVideos({ search, category })
      .then(setVideos)
      .catch(() => setError("Couldn't load videos. Try again."))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    load();
  }, [category]);

  function handleSearch(e) {
    e.preventDefault();
    load();
  }

  async function handleFavorite(video) {
    setVideos((prev) =>
      prev.map((v) => (v.id === video.id ? { ...v, is_favorited: !v.is_favorited } : v))
    );
    await toggleFavorite(video.id);
  }

  function handleWatch(video) {
    logWatch(video.id);
    window.open(video.video_url, "_blank");
  }

  return (
    <div className="max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-green-400">Farming Videos</h1>
        <p className="text-gray-500 text-sm mt-1">Learn from a library of farming videos.</p>
      </div>

      <div className="flex flex-wrap gap-2">
        <form onSubmit={handleSearch} className="flex gap-2 flex-1 min-w-[200px]">
          <input
            className="flex-1 rounded-lg border border-leaf-100 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-leaf-500"
            placeholder="Search videos…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button type="submit" className="rounded-lg bg-green-600 text-white px-4 py-2 text-sm font-medium hover:bg-green-700 transition">
            Search
          </button>
        </form>
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="rounded-lg border border-leaf-100 bg-white px-3 py-2 text-sm"
        >
          {CATEGORIES.map((c) => <option key={c.value} value={c.value}>{c.label}</option>)}
        </select>
      </div>

      {loading ? (
        <Spinner label="Loading videos…" />
      ) : error ? (
        <ErrorState message={error} onRetry={load} />
      ) : videos.length === 0 ? (
        <EmptyState icon="🎬" title="No videos found" message="Try a different search or category." />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {videos.map((v) => (
            <Card key={v.id}>
              <div className="flex items-start justify-between gap-2">
                <h3 className="font-bold text-gray-100 text-sm">{v.title}</h3>
                <button onClick={() => handleFavorite(v)} className="text-lg shrink-0">
                  {v.is_favorited ? "❤️" : "🤍"}
                </button>
              </div>
              <p className="text-xs text-gray-500 mt-1">{v.description}</p>
              <button
                onClick={() => handleWatch(v)}
                className="mt-3 text-sm text-green-400 hover:underline"
              >
                ▶ Watch
              </button>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
