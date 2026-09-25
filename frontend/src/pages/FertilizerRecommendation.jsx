import { useState } from "react";
import { recommendFertilizers } from "../services/fertilizers";
import FormField from "../components/FormField";
import Card from "../components/Card";

const inputClass =
  "w-full rounded-lg border border-gray-600 bg-gray-700 text-gray-100 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500";

const GROWTH_STAGES = ["seedling", "vegetative", "flowering", "fruiting"];

export default function FertilizerRecommendation() {
  const [form, setForm] = useState({
    crop: "", soil_type: "", n: "", p: "", k: "", ph: "", growth_stage: "", land_area: "",
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
        crop: form.crop,
        soil_type: form.soil_type,
        growth_stage: form.growth_stage,
        n: numOrUndefined(form.n),
        p: numOrUndefined(form.p),
        k: numOrUndefined(form.k),
        ph: numOrUndefined(form.ph),
        land_area: numOrUndefined(form.land_area),
      };
      const data = await recommendFertilizers(payload);
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
        <h1 className="text-2xl font-bold text-green-400">Fertilizer Recommendation</h1>
        <p className="text-gray-500 text-sm mt-1">
          Tell us your crop and current soil NPK levels to see what's needed.
        </p>
      </div>

      <Card>
        <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 gap-x-4">
          <FormField label="Crop">
            <input className={inputClass} value={form.crop}
              onChange={(e) => setForm({ ...form, crop: e.target.value })}
              placeholder="e.g. cotton, rice, wheat" />
          </FormField>
          <FormField label="Growth stage">
            <select className={inputClass} value={form.growth_stage}
              onChange={(e) => setForm({ ...form, growth_stage: e.target.value })}>
              <option value="">Not sure</option>
              {GROWTH_STAGES.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
          </FormField>
          <FormField label="Current Nitrogen (N, kg/ha)">
            <input type="number" className={inputClass} value={form.n}
              onChange={(e) => setForm({ ...form, n: e.target.value })} />
          </FormField>
          <FormField label="Current Phosphorus (P, kg/ha)">
            <input type="number" className={inputClass} value={form.p}
              onChange={(e) => setForm({ ...form, p: e.target.value })} />
          </FormField>
          <FormField label="Current Potassium (K, kg/ha)">
            <input type="number" className={inputClass} value={form.k}
              onChange={(e) => setForm({ ...form, k: e.target.value })} />
          </FormField>
          <FormField label="Soil pH">
            <input type="number" step="0.1" className={inputClass} value={form.ph}
              onChange={(e) => setForm({ ...form, ph: e.target.value })} />
          </FormField>
          <FormField label="Land area (acres)">
            <input type="number" step="0.01" className={inputClass} value={form.land_area}
              onChange={(e) => setForm({ ...form, land_area: e.target.value })} />
          </FormField>

          {error && <p className="sm:col-span-2 text-sm text-red-600 mb-3">{error}</p>}

          <button type="submit" disabled={loading}
            className="sm:col-span-2 rounded-lg bg-green-600 text-white px-5 py-2 font-medium hover:bg-green-700 disabled:opacity-60 transition">
            {loading ? "Analyzing…" : "Get Recommendations"}
          </button>
        </form>
      </Card>

      {result && (
        <div className="space-y-3">
          <h2 className="text-lg font-semibold text-green-400">
            {result.predicted_fertilizers.length > 0 ? "Recommended fertilizers" : "No deficiency detected"}
          </h2>
          {result.predicted_fertilizers.length === 0 && (
            <Card>
              <p className="text-sm text-gray-400">
                Your reported NPK levels look sufficient for this crop — no additional fertilizer needed right now.
              </p>
            </Card>
          )}
          {result.predicted_fertilizers.map((fert, i) => (
            <Card key={i}>
              <div className="flex items-start justify-between mb-2">
                <h3 className="font-bold text-gray-100">{fert.label}</h3>
                <span className="text-xs bg-leaf-100 text-green-400 rounded-full px-2 py-1">
                  {fert.details.fertilizer_type}
                </span>
              </div>
              <ul className="text-sm text-gray-400 space-y-1">
                <li>Estimated quantity: {fert.details.estimated_quantity_kg} kg</li>
                <li>Apply: {fert.details.application_stage}</li>
                <li>Method: {fert.details.application_method}</li>
                <li className="pt-1 text-amber-700">⚠ {fert.details.precautions}</li>
              </ul>
            </Card>
          ))}
          <p className="text-xs text-gray-400">
            Estimates from a rule-based calculator, not a lab soil test — for precise dosing, consult
            your local agriculture extension officer.
          </p>
        </div>
      )}
    </div>
  );
}
