import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth, roleHomePath } from "../context/AuthContext";
import ThemeToggle from "../components/ThemeToggle";
import FormField from "../components/FormField";

const ic = "w-full rounded-lg border border-gray-600 bg-gray-700 text-gray-100 px-3 py-2 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault(); setError(""); setLoading(true);
    try { const me = await login(form.email, form.password); navigate(roleHomePath(me)); }
    catch (err) { setError(err.response?.data?.detail || "Invalid email or password."); }
    finally { setLoading(false); }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 bg-gray-900">
      <div className="absolute top-4 right-4"><ThemeToggle /></div>
      <div className="w-full max-w-sm bg-gray-800 rounded-2xl shadow-xl border border-gray-700 p-8">
        <h1 className="text-2xl font-bold text-green-400 mb-1">🌾 Smart Kisaan</h1>
        <p className="text-sm text-gray-400 mb-6">Log in to your dashboard</p>
        <form onSubmit={handleSubmit}>
          <FormField label="Email">
            <input type="email" required className={ic} value={form.email}
              onChange={e => setForm({ ...form, email: e.target.value })} placeholder="you@example.com" />
          </FormField>
          <FormField label="Password">
            <input type="password" required className={ic} value={form.password}
              onChange={e => setForm({ ...form, password: e.target.value })} placeholder="••••••••" />
          </FormField>
          {error && <p className="text-sm text-red-400 mb-4">{error}</p>}
          <button type="submit" disabled={loading}
            className="w-full rounded-lg bg-green-600 text-white py-2 font-medium hover:bg-green-700 disabled:opacity-60 transition">
            {loading ? "Logging in…" : "Log In"}
          </button>
        </form>
        <p className="text-sm text-gray-500 mt-6 text-center">
          New here? <Link to="/register" className="text-green-400 font-medium">Create an account</Link>
        </p>
      </div>
    </div>
  );
}
