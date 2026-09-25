import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { getMarketPrices, getMarketTrend } from "../services/market";
import Card from "../components/Card";
import { Spinner, EmptyState, ErrorState } from "../components/StateComponents";

const SORT_OPTIONS = [
  { value: "", label: "Default" },
  { value: "price_desc", label: "Price: high to low" },
  { value: "price_asc", label: "Price: low to high" },
  { value: "date_desc", label: "Newest first" },
];

export default function MarketPrices() {
  const [prices, setPrices] = useState([]);
  const [cropFilter, setCropFilter] = useState("");
  const [marketFilter, setMarketFilter] = useState("");
  const [sort, setSort] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedCrop, setSelectedCrop] = useState(null);
  const [trend, setTrend] = useState(null);

  async function load() {
    setLoading(true);
    setError("");
    try {
      const data = await getMarketPrices({ crop: cropFilter, market: marketFilter, sort });
      setPrices(data);
    } catch {
      setError("Couldn't load market prices. Check your connection and try again.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  function handleFilterSubmit(e) {
    e.preventDefault();
    load();
  }

  async function handleViewTrend(cropName) {
    setSelectedCrop(cropName);
    setTrend(null);
    const data = await getMarketTrend(cropName);
    setTrend(data);
  }

  return (
    <div className="max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-green-400">Market Prices</h1>
        <p className="text-gray-500 text-sm mt-1">Latest prices across markets — click a row for price history.</p>
      </div>

      <form onSubmit={handleFilterSubmit} className="flex flex-wrap gap-2">
        <input
          className="flex-1 min-w-[140px] rounded-lg border border-leaf-100 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-leaf-500"
          placeholder="Filter by crop…"
          value={cropFilter}
          onChange={(e) => setCropFilter(e.target.value)}
        />
        <input
          className="flex-1 min-w-[140px] rounded-lg border border-leaf-100 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-leaf-500"
          placeholder="Filter by market…"
          value={marketFilter}
          onChange={(e) => setMarketFilter(e.target.value)}
        />
        <select
          className="rounded-lg border border-leaf-100 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-leaf-500"
          value={sort}
          onChange={(e) => setSort(e.target.value)}
        >
          {SORT_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
        </select>
        <button type="submit" className="rounded-lg bg-green-600 text-white px-4 py-2 text-sm font-medium hover:bg-green-700 transition">
          Apply
        </button>
      </form>

      {loading ? (
        <Spinner label="Loading prices…" />
      ) : error ? (
        <ErrorState message={error} onRetry={load} />
      ) : (
        <Card>
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-gray-400 border-b border-leaf-100">
                <th className="pb-2">Crop</th>
                <th className="pb-2">Market</th>
                <th className="pb-2">Price</th>
                <th className="pb-2">Range</th>
                <th className="pb-2">Date</th>
              </tr>
            </thead>
            <tbody>
              {prices.map((p) => (
                <tr
                  key={p.id}
                  className="border-b border-leaf-50 last:border-0 cursor-pointer hover:bg-leaf-50"
                  onClick={() => handleViewTrend(p.crop_name)}
                >
                  <td className="py-2 font-medium text-gray-100">{p.crop_name}</td>
                  <td className="py-2 text-gray-400">{p.market_name}</td>
                  <td className="py-2 text-green-400 font-semibold">₹{p.current_price}</td>
                  <td className="py-2 text-gray-400 text-xs">₹{p.min_price}–₹{p.max_price}</td>
                  <td className="py-2 text-gray-400 text-xs">{p.recorded_date}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {prices.length === 0 && (
            <EmptyState icon="📈" title="No prices found" message="Try different search filters." />
          )}
        </Card>
      )}

      {selectedCrop && (
        <Card title={`${selectedCrop} — price history`}>
          {trend ? (
            trend.history.length > 1 ? (
              <>
                <ResponsiveContainer width="100%" height={200}>
                  <LineChart data={trend.history}>
                    <XAxis dataKey="date" tick={{ fontSize: 11 }} />
                    <YAxis tick={{ fontSize: 11 }} />
                    <Tooltip />
                    <Line type="monotone" dataKey="price" stroke="#16a34a" strokeWidth={2} dot={false} />
                  </LineChart>
                </ResponsiveContainer>
                <p className="text-xs text-gray-400 mt-2">
                  Historical prices — not a forecast or prediction.
                </p>
              </>
            ) : (
              <p className="text-sm text-gray-500">Not enough history yet for a trend line.</p>
            )
          ) : (
            <p className="text-sm text-gray-500">Loading history…</p>
          )}
        </Card>
      )}
    </div>
  );
}
