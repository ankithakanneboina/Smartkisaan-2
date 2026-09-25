import { useEffect, useState } from "react";
import { getSchemes } from "../services/schemes";
import Card from "../components/Card";
import { Spinner, EmptyState, ErrorState } from "../components/StateComponents";

export default function Schemes() {
  const [schemes, setSchemes] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [expanded, setExpanded] = useState(null);

  function load() {
    setLoading(true);
    setError("");
    getSchemes({ search })
      .then(setSchemes)
      .catch(() => setError("Couldn't load schemes. Try again."))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    load();
  }, []);

  function handleSearch(e) {
    e.preventDefault();
    load();
  }

  return (
    <div className="max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-green-400">Government Schemes</h1>
        <p className="text-gray-500 text-sm mt-1">Browse schemes and check eligibility.</p>
      </div>

      <form onSubmit={handleSearch} className="flex gap-2">
        <input
          className="flex-1 rounded-lg border border-leaf-100 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-leaf-500"
          placeholder="Search schemes…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <button type="submit" className="rounded-lg bg-green-600 text-white px-4 py-2 text-sm font-medium hover:bg-green-700 transition">
          Search
        </button>
      </form>

      {loading ? (
        <Spinner label="Loading schemes…" />
      ) : error ? (
        <ErrorState message={error} onRetry={load} />
      ) : schemes.length === 0 ? (
        <EmptyState icon="📜" title="No schemes found" message="Your administrator can add schemes via the admin panel." />
      ) : (
        schemes.map((s) => (
          <Card key={s.id}>
            <div className="flex items-center justify-between cursor-pointer" onClick={() => setExpanded(expanded === s.id ? null : s.id)}>
              <h3 className="font-bold text-gray-100">{s.name}</h3>
              <span className="text-green-500 text-sm">{expanded === s.id ? "Hide" : "Details"}</span>
            </div>
            <p className="text-sm text-gray-400 mt-1">{s.description}</p>
            {expanded === s.id && (
              <dl className="text-sm text-gray-400 space-y-2 mt-3 pt-3 border-t border-leaf-50">
                {s.eligibility && <div><dt className="font-medium text-gray-700">Eligibility</dt><dd>{s.eligibility}</dd></div>}
                {s.benefits && <div><dt className="font-medium text-gray-700">Benefits</dt><dd>{s.benefits}</dd></div>}
                {s.required_documents && <div><dt className="font-medium text-gray-700">Required documents</dt><dd>{s.required_documents}</dd></div>}
                {s.application_process && <div><dt className="font-medium text-gray-700">How to apply</dt><dd>{s.application_process}</dd></div>}
                {s.official_link && (
                  <a href={s.official_link} target="_blank" rel="noreferrer" className="text-green-500 underline block">
                    Official scheme page →
                  </a>
                )}
              </dl>
            )}
          </Card>
        ))
      )}
    </div>
  );
}
