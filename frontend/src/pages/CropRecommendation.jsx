import { useState } from "react";
import { recommendCrops } from "../services/crops";
import FormField from "../components/FormField";
import Card from "../components/Card";

const inputClass =
  "w-full rounded-lg border border-gray-600 bg-gray-700 text-gray-100 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500";

const SOIL_TYPES = ["alluvial", "black", "red", "laterite", "sandy", "clay", "loamy"];
const SEASONS = ["kharif", "rabi", "zaid"];

export default function CropRecommendation() {
  const [form, setForm] = useState({
    soil_type: "", n: "", p: "", k: "", ph: "", temperature: "",
    humidity: "", rainfall: "", season: "", land_area: "", irrigation_available: false,
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function numOrUndefined(v) {
    return v === "" ? undefined : Number(v);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const payload = {
        soil_type: form.soil_type,
        season: form.season,
        n: numOrUndefined(form.n),
        p: numOrUndefined(form.p),
        k: numOrUndefined(form.k),
        ph: numOrUndefined(form.ph),
        temperature: numOrUndefined(form.temperature),
        humidity: numOrUndefined(form.humidity),
        rainfall: numOrUndefined(form.rainfall),
        land_area: numOrUndefined(form.land_area),
        irrigation_available: form.irrigation_available,
      };
      const data = await recommendCrops(payload);
      setResult(data);
    } catch (err) {
      setError("Couldn't get a recommendation. Check your inputs and try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-green-400">Crop Recommendation</h1>
        <p className="text-gray-500 text-sm mt-1">
          Enter what you know about your soil and climate — leave anything blank if unsure.
        </p>
      </div>

      <Card>
        <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 gap-x-4">
          <FormField label="Soil type">
            <select className={inputClass} value={form.soil_type}
              onChange={(e) => setForm({ ...form, soil_type: e.target.value })}>
              <option value="">Not sure</option>
              {SOIL_TYPES.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
          </FormField>
          <FormField label="Season">
            <select className={inputClass} value={form.season}
              onChange={(e) => setForm({ ...form, season: e.target.value })}>
              <option value="">Not sure</option>
              {SEASONS.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
          </FormField>
          <FormField label="Nitrogen (N, kg/ha)">
            <input type="number" className={inputClass} value={form.n}
              onChange={(e) => setForm({ ...form, n: e.target.value })} />
          </FormField>
          <FormField label="Phosphorus (P, kg/ha)">
            <input type="number" className={inputClass} value={form.p}
              onChange={(e) => setForm({ ...form, p: e.target.value })} />
          </FormField>
          <FormField label="Potassium (K, kg/ha)">
            <input type="number" className={inputClass} value={form.k}
              onChange={(e) => setForm({ ...form, k: e.target.value })} />
          </FormField>
          <FormField label="Soil pH">
            <input type="number" step="0.1" className={inputClass} value={form.ph}
              onChange={(e) => setForm({ ...form, ph: e.target.value })} />
          </FormField>
          <FormField label="Avg temperature (°C)">
            <input type="number" className={inputClass} value={form.temperature}
              onChange={(e) => setForm({ ...form, temperature: e.target.value })} />
          </FormField>
          <FormField label="Avg humidity (%)">
            <input type="number" className={inputClass} value={form.humidity}
              onChange={(e) => setForm({ ...form, humidity: e.target.value })} />
          </FormField>
          <FormField label="Rainfall (mm)">
            <input type="number" className={inputClass} value={form.rainfall}
              onChange={(e) => setForm({ ...form, rainfall: e.target.value })} />
          </FormField>
          <FormField label="Land area (acres)">
            <input type="number" step="0.01" className={inputClass} value={form.land_area}
              onChange={(e) => setForm({ ...form, land_area: e.target.value })} />
          </FormField>

          <label className="flex items-center gap-2 sm:col-span-2 mb-4 text-sm text-gray-400">
            <input type="checkbox" checked={form.irrigation_available}
              onChange={(e) => setForm({ ...form, irrigation_available: e.target.checked })} />
            Irrigation available
          </label>

          {error && <p className="sm:col-span-2 text-sm text-red-600 mb-3">{error}</p>}

          <button type="submit" disabled={loading}
            className="sm:col-span-2 rounded-lg bg-green-600 text-white px-5 py-2 font-medium hover:bg-green-700 disabled:opacity-60 transition">
            {loading ? "Analyzing…" : "Get Recommendations"}
          </button>
        </form>
      </Card>

      {result && (
        <div className="space-y-3">
          <h2 className="text-lg font-semibold text-green-400">Recommended crops</h2>
          {result.predicted_crops.map((crop, i) => (
            <Card key={i}>
              <div className="flex items-start justify-between mb-2">
                <h3 className="font-bold text-gray-100">{crop.label}</h3>
                <span className="text-xs bg-leaf-100 text-green-400 rounded-full px-2 py-1">
                  {Math.round(crop.confidence * 100)}% match
                </span>
              </div>
              <ul className="text-sm text-gray-400 space-y-1">
                <li>Duration: {crop.details.growing_duration_days} days</li>
                <li>Water need: {crop.details.water_requirement}</li>
                <li>Soil: {crop.details.soil_requirement}</li>
                <li>Season: {crop.details.suitable_season}</li>
                <li className="pt-1 text-gray-500">{crop.details.farming_tips}</li>
              </ul>
            </Card>
          ))}
          <p className="text-xs text-gray-400">
            Based on a rule-based reference table, not a trained model — treat as a starting point,
            not a guarantee.
          </p>
        </div>
      )}
    </div>
  );
}
