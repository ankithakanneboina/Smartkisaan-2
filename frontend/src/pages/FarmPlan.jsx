import { useEffect, useState } from "react";
import { generateFarmPlan, getFarmPlans, updateTask, updatePlanStatus } from "../services/farmPlan";
import FormField from "../components/FormField";
import Card from "../components/Card";

const inputClass =
  "w-full rounded-lg border border-gray-600 bg-gray-700 text-gray-100 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500";

export default function FarmPlan() {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({ crop: "", season: "", start_date: "" });
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState("");

  function loadPlans() {
    getFarmPlans().then(setPlans).finally(() => setLoading(false));
  }

  useEffect(() => {
    loadPlans();
  }, []);

  async function handleGenerate(e) {
    e.preventDefault();
    setGenerating(true);
    setError("");
    try {
      await generateFarmPlan(form);
      setForm({ crop: "", season: "", start_date: "" });
      loadPlans();
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Couldn't generate a plan — check the crop name matches your catalog."
      );
    } finally {
      setGenerating(false);
    }
  }

  async function handleToggleTask(task) {
    setPlans((prev) =>
      prev.map((p) => ({
        ...p,
        tasks: p.tasks.map((t) => (t.id === task.id ? { ...t, is_done: !t.is_done } : t)),
      }))
    );
    await updateTask(task.id, { is_done: !task.is_done });
  }

  async function handleMarkCompleted(planId) {
    await updatePlanStatus(planId, "completed");
    loadPlans();
  }

  return (
    <div className="max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-green-400">My Farm Plan</h1>
        <p className="text-gray-500 text-sm mt-1">
          Generate a week-by-week plan for your crop, then track it as you go.
        </p>
      </div>

      <Card title="Generate a new plan">
        <form onSubmit={handleGenerate} className="grid grid-cols-1 sm:grid-cols-3 gap-x-4">
          <FormField label="Crop">
            <input required className={inputClass} value={form.crop}
              onChange={(e) => setForm({ ...form, crop: e.target.value })}
              placeholder="e.g. Cotton" />
          </FormField>
          <FormField label="Season (optional)">
            <input className={inputClass} value={form.season}
              onChange={(e) => setForm({ ...form, season: e.target.value })} placeholder="Kharif" />
          </FormField>
          <FormField label="Start date">
            <input type="date" required className={inputClass} value={form.start_date}
              onChange={(e) => setForm({ ...form, start_date: e.target.value })} />
          </FormField>
          {error && <p className="sm:col-span-3 text-sm text-red-600 mb-3">{error}</p>}
          <button type="submit" disabled={generating}
            className="sm:col-span-3 rounded-lg bg-green-600 text-white px-5 py-2 font-medium hover:bg-green-700 disabled:opacity-60 transition">
            {generating ? "Generating…" : "Generate Plan"}
          </button>
        </form>
      </Card>

      {loading ? (
        <p className="text-green-500">Loading your plans…</p>
      ) : plans.length === 0 ? (
        <p className="text-sm text-gray-500">No plans yet — generate one above to get started.</p>
      ) : (
        plans.map((plan) => (
          <Card key={plan.id}>
            <div className="flex items-center justify-between mb-3">
              <div>
                <h3 className="font-bold text-gray-100">{plan.title}</h3>
                <span className={`text-xs rounded-full px-2 py-0.5 ${
                  plan.status === "completed" ? "bg-leaf-100 text-green-400" : "bg-amber-100 text-amber-700"
                }`}>
                  {plan.status}
                </span>
              </div>
              {plan.status === "active" && (
                <button onClick={() => handleMarkCompleted(plan.id)}
                  className="text-xs text-green-400 hover:underline">
                  Mark completed
                </button>
              )}
            </div>
            <ul className="space-y-2">
              {plan.tasks.map((task) => (
                <li key={task.id} className="flex items-start gap-2 text-sm">
                  <input type="checkbox" checked={task.is_done} onChange={() => handleToggleTask(task)}
                    className="mt-1" />
                  <div className={task.is_done ? "line-through text-gray-400" : "text-gray-700"}>
                    <span className="font-medium">Week {task.week_number}: {task.title}</span>
                    {task.due_date && <span className="text-gray-400"> — {task.due_date}</span>}
                    <p className="text-gray-500 text-xs mt-0.5">{task.description}</p>
                  </div>
                </li>
              ))}
            </ul>
          </Card>
        ))
      )}
    </div>
  );
}
