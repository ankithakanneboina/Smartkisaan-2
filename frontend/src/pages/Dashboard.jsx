import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { getMyProfile } from "../services/farmers";
import { getCurrentWeather } from "../services/weather";
import { getRecentActivities } from "../services/activities";
import { getUpcomingReminders, markReminderDone } from "../services/reminders";
import Card from "../components/Card";
import { Spinner } from "../components/StateComponents";

const ACTIVITY_ICONS = { sowing:"🌱", irrigation:"💧", fertilizer:"🧪", pest_observation:"🐛", harvest:"🌾", expense:"💰", other:"📋" };

export default function Dashboard() {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [weather, setWeather] = useState(null);
  const [weatherError, setWeatherError] = useState("");
  const [activities, setActivities] = useState([]);
  const [reminders, setReminders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const p = await getMyProfile();
        if (cancelled) return;
        setProfile(p);
        try { const w = await getCurrentWeather(p.location || undefined); if (!cancelled) setWeather(w); }
        catch (err) { if (!cancelled) setWeatherError(err.response?.data?.detail || "Add location in profile to see weather."); }
      } finally { if (!cancelled) setLoading(false); }
    }
    load();
    getRecentActivities().then(a => !cancelled && setActivities(a));
    getUpcomingReminders().then(r => !cancelled && setReminders(r));
    return () => { cancelled = true; };
  }, []);

  async function handleMarkDone(id) {
    setReminders(prev => prev.filter(r => r.id !== id));
    try { await markReminderDone(id); } catch { getUpcomingReminders().then(setReminders); }
  }

  if (loading) return <Spinner label="Loading your dashboard…" />;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-green-400">Welcome back, {profile?.full_name || user?.username} 👋</h1>
        <p className="text-gray-500 text-sm mt-1">Here's what's happening on your farm today.</p>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <Card title="Weather" className="sm:col-span-2">
          {weather ? (
            <a href="/weather" className="block hover:opacity-90 transition">
              <div className="flex items-center gap-6">
                <div className="text-4xl font-bold text-green-400">{weather.temperature_c}°C</div>
                <div className="text-sm text-gray-400 space-y-0.5">
                  <div className="text-gray-200">{weather.location_name}</div>
                  <div>Humidity: {weather.humidity_percent}%</div>
                  <div>Rain: {weather.rainfall_mm} mm</div>
                  {weather.provider === "mock" && <div className="text-xs text-yellow-500">Sample data — add WEATHER_API_KEY for live</div>}
                  {weather.alerts?.length > 0 && <div className="text-xs text-red-400">Alerts: {weather.alerts.join(", ")}</div>}
                </div>
              </div>
            </a>
          ) : <p className="text-sm text-gray-500">{weatherError}</p>}
        </Card>

        <Card title="Your Farm">
          {profile?.land_area_acres || profile?.soil_type ? (
            <ul className="text-sm text-gray-400 space-y-1">
              <li>Land: <span className="text-gray-200">{profile.land_area_acres ?? "—"} acres</span></li>
              <li>Soil: <span className="text-gray-200">{profile.soil_type || "—"}</span></li>
              <li>Irrigation: <span className="text-gray-200">{profile.irrigation_type || "—"}</span></li>
              <li>District: <span className="text-gray-200">{profile.district || "—"}</span></li>
            </ul>
          ) : (
            <p className="text-sm text-gray-500">Complete your <a href="/profile" className="text-green-400 underline">farm profile</a> to unlock recommendations.</p>
          )}
        </Card>

        <Card title="Recent activities">
          {activities.length > 0 ? (
            <ul className="text-sm text-gray-400 space-y-2">
              {activities.map(a => (
                <li key={a.id} className="flex items-start gap-2">
                  <span>{ACTIVITY_ICONS[a.activity_type] || "📋"}</span>
                  <span><span className="text-gray-200">{a.crop_name || "General"}</span> — {a.activity_type.replace("_"," ")} ({a.activity_date})</span>
                </li>
              ))}
            </ul>
          ) : <p className="text-sm text-gray-500">No activity logged yet.</p>}
        </Card>

        <Card title="Reminders">
          {reminders.length > 0 ? (
            <ul className="text-sm text-gray-400 space-y-2">
              {reminders.map(r => (
                <li key={r.id} className="flex items-center justify-between gap-2">
                  <span><span className="text-gray-200">{r.title}</span>{r.due_date && <span className="text-gray-500"> — {r.due_date}</span>}</span>
                  <button onClick={() => handleMarkDone(r.id)} className="text-xs text-green-400 hover:underline shrink-0">Done</button>
                </li>
              ))}
            </ul>
          ) : <p className="text-sm text-gray-500">No upcoming reminders.</p>}
        </Card>

        <Card title="Quick links">
          <div className="flex flex-col gap-2 text-sm">
            <a href="/assistant" className="text-green-400 hover:underline">💬 Ask AI Assistant</a>
            <a href="/crops/recommend" className="text-green-400 hover:underline">🌾 Crop recommendation</a>
            <a href="/fertilizers/recommend" className="text-green-400 hover:underline">🧪 Fertilizer advice</a>
            <a href="/farm-plan" className="text-green-400 hover:underline">📅 View farm plan</a>
            <a href="/market" className="text-green-400 hover:underline">📈 Market prices</a>
            <a href="/profit" className="text-green-400 hover:underline">💰 Profit calculator</a>
            <a href="/diseases/detect" className="text-green-400 hover:underline">🔬 Disease check</a>
            <a href="/schemes" className="text-green-400 hover:underline">📜 Govt schemes</a>
            <a href="/marketplace" className="text-green-400 hover:underline">🛒 Marketplace</a>
            <a href="/community" className="text-green-400 hover:underline">👥 Community</a>
          </div>
        </Card>
      </div>
    </div>
  );
}
