import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth, roleHomePath } from "../context/AuthContext";
import { sendOtp, verifyOtp } from "../services/otp";
import ThemeToggle from "../components/ThemeToggle";

const ic = "w-full rounded-lg border border-gray-600 bg-gray-700 text-gray-100 px-3 py-2 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [phone, setPhone] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [otpInput, setOtpInput] = useState("");
  const [verifiedPhone, setVerifiedPhone] = useState("");
  const [form, setForm] = useState({ username: "", email: "", password: "", password2: "", role: "buyer" });
  const [errors, setErrors] = useState({});
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSendOtp(e) {
    e.preventDefault(); setErrors({}); setMsg(""); setLoading(true);
    try {
      const d = await sendOtp(phone);
      setSessionId(d.session_id); setVerifiedPhone(d.phone_number);
      setMsg("OTP sent! Check the Django server console (Terminal 1).");
      setStep(2);
    } catch (err) { setErrors({ detail: err.response?.data?.detail || "Couldn't send OTP." }); }
    finally { setLoading(false); }
  }

  async function handleVerifyOtp(e) {
    e.preventDefault(); setErrors({}); setLoading(true);
    try { await verifyOtp(sessionId, otpInput); setMsg("Mobile verified ✓"); setStep(3); }
    catch (err) { setErrors({ detail: err.response?.data?.detail || "Incorrect OTP." }); }
    finally { setLoading(false); }
  }

  async function handleRegister(e) {
    e.preventDefault(); setErrors({}); setLoading(true);
    try {
      const me = await register({ ...form, phone_number: verifiedPhone, otp_session_id: sessionId });
      navigate(roleHomePath(me));
    } catch (err) { setErrors(err.response?.data?.fields || err.response?.data || { detail: "Registration failed." }); }
    finally { setLoading(false); }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-10 bg-gray-900">
      <div className="absolute top-4 right-4"><ThemeToggle /></div>
      <div className="w-full max-w-sm bg-gray-800 rounded-2xl shadow-xl border border-gray-700 p-8">
        <h1 className="text-2xl font-bold text-green-400 mb-1">🌱 Join Smart Kisaan</h1>

        {/* Step indicator */}
        <div className="flex items-center gap-2 mb-6">
          {[1, 2, 3].map(s => (
            <div key={s} className="flex items-center gap-1">
              <div className={`w-6 h-6 rounded-full text-xs flex items-center justify-center font-bold
                ${step >= s ? "bg-green-600 text-white" : "bg-gray-700 text-gray-500"}`}>
                {step > s ? "✓" : s}
              </div>
              {s < 3 && <div className={`w-6 h-0.5 ${step > s ? "bg-green-600" : "bg-gray-700"}`} />}
            </div>
          ))}
          <span className="text-xs text-gray-500 ml-1">
            {step === 1 ? "Enter mobile" : step === 2 ? "Verify OTP" : "Create account"}
          </span>
        </div>

        {msg && <p className="text-sm text-green-400 mb-4 bg-green-900 bg-opacity-30 rounded-lg px-3 py-2">{msg}</p>}
        {errors.detail && <p className="text-sm text-red-400 mb-4">{errors.detail}</p>}

        {step === 1 && (
          <form onSubmit={handleSendOtp}>
            <label className="block mb-4">
              <span className="block text-sm font-medium text-gray-300 mb-1">Mobile number</span>
              <input type="tel" required placeholder="9998887777" className={ic}
                value={phone} onChange={e => setPhone(e.target.value)} />
              <span className="text-xs text-gray-500 mt-1 block">OTP will show in Django console (Terminal 1)</span>
            </label>
            <button type="submit" disabled={loading}
              className="w-full rounded-lg bg-green-600 text-white py-2 font-medium hover:bg-green-700 disabled:opacity-60 transition">
              {loading ? "Sending…" : "Send OTP"}
            </button>
          </form>
        )}

        {step === 2 && (
          <form onSubmit={handleVerifyOtp}>
            <p className="text-sm text-gray-400 mb-4">Enter OTP for <strong className="text-gray-200">{verifiedPhone}</strong></p>
            <label className="block mb-4">
              <span className="block text-sm font-medium text-gray-300 mb-1">OTP</span>
              <input type="text" required maxLength={6} placeholder="123456"
                className={ic + " tracking-widest text-center text-xl font-bold"}
                value={otpInput} onChange={e => setOtpInput(e.target.value.replace(/\D/g, "").slice(0, 6))} />
            </label>
            <button type="submit" disabled={loading || otpInput.length !== 6}
              className="w-full rounded-lg bg-green-600 text-white py-2 font-medium hover:bg-green-700 disabled:opacity-60 transition">
              {loading ? "Verifying…" : "Verify OTP"}
            </button>
            <button type="button" onClick={() => { setStep(1); setOtpInput(""); setMsg(""); }}
              className="w-full mt-2 text-sm text-green-400 hover:underline">← Change number / Resend</button>
          </form>
        )}

        {step === 3 && (
          <form onSubmit={handleRegister}>
            <p className="text-sm text-green-400 mb-4">✓ Mobile verified — {verifiedPhone}</p>
            {[
              { label: "I am a", type: "select", key: "role" },
              { label: "Username", type: "text", key: "username" },
              { label: "Email", type: "email", key: "email" },
              { label: "Password", type: "password", key: "password" },
              { label: "Confirm password", type: "password", key: "password2" },
            ].map(f => (
              <label key={f.key} className="block mb-3">
                <span className="block text-sm font-medium text-gray-300 mb-1">{f.label}</span>
                {f.type === "select" ? (
                  <select className={ic} value={form.role} onChange={e => setForm({ ...form, role: e.target.value })}>
                    <option value="buyer">Buyer — browsing &amp; ordering</option>
                    <option value="farmer">Farmer — selling my produce</option>
                  </select>
                ) : (
                  <input type={f.type} required className={ic} value={form[f.key]}
                    onChange={e => setForm({ ...form, [f.key]: e.target.value })} />
                )}
                {errors[f.key] && <span className="text-xs text-red-400 mt-1 block">{errors[f.key][0]}</span>}
              </label>
            ))}
            <button type="submit" disabled={loading}
              className="w-full rounded-lg bg-green-600 text-white py-2 font-medium hover:bg-green-700 disabled:opacity-60 transition">
              {loading ? "Creating…" : "Create Account"}
            </button>
          </form>
        )}

        <p className="text-sm text-gray-500 mt-6 text-center">
          Already have an account? <Link to="/login" className="text-green-400 font-medium">Log in</Link>
        </p>
      </div>
    </div>
  );
}
