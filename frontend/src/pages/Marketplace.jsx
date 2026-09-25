import { useEffect, useState } from "react";
import { getProducts, toggleWishlist } from "../services/marketplace";
import Card from "../components/Card";
import { Spinner, EmptyState, ErrorState } from "../components/StateComponents";

const CATEGORIES = [
  { value: "", label: "All categories" },
  { value: "seeds", label: "Seeds" },
  { value: "fertilizers", label: "Fertilizers" },
  { value: "equipment", label: "Farming equipment" },
  { value: "irrigation_equipment", label: "Irrigation equipment" },
  { value: "organic_products", label: "Organic products" },
];

export default function Marketplace() {
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  function load() {
    setLoading(true);
    setError("");
    getProducts({ search, category })
      .then(setProducts)
      .catch(() => setError("Couldn't load products. Try again."))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    load();
  }, [category]);

  function handleSearch(e) {
    e.preventDefault();
    load();
  }

  async function handleWishlist(product) {
    setProducts((prev) =>
      prev.map((p) => (p.id === product.id ? { ...p, is_wishlisted: !p.is_wishlisted } : p))
    );
    await toggleWishlist(product.id);
  }

  return (
    <div className="max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-green-400">Marketplace</h1>
        <p className="text-gray-500 text-sm mt-1">Seeds, fertilizers, equipment, and more.</p>
      </div>

      <div className="flex flex-wrap gap-2">
        <form onSubmit={handleSearch} className="flex gap-2 flex-1 min-w-[200px]">
          <input
            className="flex-1 rounded-lg border border-leaf-100 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-leaf-500"
            placeholder="Search products…"
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
        <Spinner label="Loading products…" />
      ) : error ? (
        <ErrorState message={error} onRetry={load} />
      ) : products.length === 0 ? (
        <EmptyState icon="🛒" title="No products found" message="Try a different search or category." />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {products.map((p) => (
            <Card key={p.id}>
              <div className="flex items-start justify-between gap-2">
                <h3 className="font-bold text-gray-100 text-sm">{p.name}</h3>
                <button onClick={() => handleWishlist(p)} className="text-lg shrink-0">
                  {p.is_wishlisted ? "❤️" : "🤍"}
                </button>
              </div>
              <p className="text-xs text-gray-500 mt-1">{p.description}</p>
              <div className="mt-3 flex items-center justify-between">
                <span className="font-semibold text-green-400">₹{p.price} <span className="text-xs text-gray-400 font-normal">{p.unit}</span></span>
              </div>
              <p className="text-xs text-gray-400 mt-1">Seller: {p.seller_name}</p>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
