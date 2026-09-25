import { useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { calculateProfit } from "../services/profit";
import FormField from "../components/FormField";
import Card from "../components/Card";

const inputClass =
  "w-full rounded-lg border border-gray-600 bg-gray-700 text-gray-100 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500";

const COST_FIELDS = [
  { key: "seed_cost", label: "Seed cost (₹)" },
  { key: "fertilizer_cost", label: "Fertilizer cost (₹)" },
  { key: "labour_cost", label: "Labour cost (₹)" },
  { key: "irrigation_cost", label: "Irrigation cost (₹)" },
  { key: "pesticide_cost", label: "Pesticide/input cost (₹)" },
  { key: "other_expenses", label: "Other expenses (₹)" },
];

export default function ProfitCalculator() {
  const [form, setForm] = useState({
    crop: "", land_area: "", seed_cost: "", fertilizer_cost: "", labour_cost: "",
    irrigation_cost: "", pesticide_cost: "", other_expenses: "",
    expected_yield: "", expected_selling_price: "",
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const payload = Object.fromEntries(
        Object.entries(form).map(([k, v]) => [k, v === "" ? undefined : v])
      );
      const data = await calculateProfit(payload);
      setResult(data);
    } catch (err) {
      setError("Couldn't calculate — check your land area, yield, and price fields.");
    } finally {
      setLoading(false);
    }
  }

  const chartData = result
    ? [
        { name: "Investment", value: Number(result.total_investment) },
        { name: "Revenue", value: Number(result.expected_revenue) },
        { name: "Profit", value: Number(result.expected_profit) },
      ]
    : [];

  return (
    <div className="max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-green-400">Profit Calculator</h1>
        <p className="text-gray-500 text-sm mt-1">Estimate your investment, revenue, and margin.</p>
      </div>

      <Card>
        <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 gap-x-4">
          <FormField label="Crop">
            <input className={inputClass} value={form.crop}
              onChange={(e) => setForm({ ...form, crop: e.target.value })} placeholder="e.g. cotton" />
          </FormField>
          <FormField label="Land area (acres)">
            <input type="number" step="0.01" required className={inputClass} value={form.land_area}
              onChange={(e) => setForm({ ...form, land_area: e.target.value })} />
          </FormField>

          {COST_FIELDS.map((f) => (
            <FormField key={f.key} label={f.label}>
              <input type="number" className={inputClass} value={form[f.key]}
                onChange={(e) => setForm({ ...form, [f.key]: e.target.value })} />
            </FormField>
          ))}

          <FormField label="Expected yield (quintals)">
            <input type="number" step="0.01" required className={inputClass} value={form.expected_yield}
              onChange={(e) => setForm({ ...form, expected_yield: e.target.value })} />
          </FormField>
          <FormField label="Expected selling price (₹/quintal)">
            <input type="number" step="0.01" required className={inputClass} value={form.expected_selling_price}
              onChange={(e) => setForm({ ...form, expected_selling_price: e.target.value })} />
          </FormField>

          {error && <p className="sm:col-span-2 text-sm text-red-600 mb-3">{error}</p>}

          <button type="submit" disabled={loading}
            className="sm:col-span-2 rounded-lg bg-green-600 text-white px-5 py-2 font-medium hover:bg-green-700 disabled:opacity-60 transition">
            {loading ? "Calculating…" : "Calculate"}
          </button>
        </form>
      </Card>

      {result && (
        <Card title="Results">
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={chartData}>
              <XAxis dataKey="name" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip formatter={(v) => `₹${v.toLocaleString("en-IN")}`} />
              <Bar dataKey="value" fill="#16a34a" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 mt-4 text-sm">
            <div><div className="text-gray-400">Total investment</div><div className="font-semibold text-gray-100">₹{result.total_investment}</div></div>
            <div><div className="text-gray-400">Expected revenue</div><div className="font-semibold text-gray-100">₹{result.expected_revenue}</div></div>
            <div><div className="text-gray-400">Expected profit</div><div className="font-semibold text-green-400">₹{result.expected_profit}</div></div>
            <div><div className="text-gray-400">Cost/acre</div><div className="font-semibold text-gray-100">₹{result.cost_per_acre}</div></div>
            <div><div className="text-gray-400">Revenue/acre</div><div className="font-semibold text-gray-100">₹{result.revenue_per_acre}</div></div>
            <div><div className="text-gray-400">Profit margin</div><div className="font-semibold text-gray-100">{result.profit_margin_percent}%</div></div>
          </div>
        </Card>
      )}
    </div>
  );
}
