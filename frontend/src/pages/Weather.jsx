import { useEffect, useState } from "react";
import { getCurrentWeather } from "../services/weather";
import { getMyProfile } from "../services/farmers";
import Card from "../components/Card";
import { Spinner, ErrorState } from "../components/StateComponents";

const ALERT_LABELS = {
  heavy_rain: "⚠️ Heavy rain expected",
  heat_wave: "🌡️ Heat wave conditions",
  strong_wind: "💨 Strong winds",
  low_rainfall: "☀️ Low rainfall — consider irrigation",
};

export default function Weather() {
  const [weather, setWeather] = useState(null);
  const [location, setLocation] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load(loc) {
    setLoading(true);
    setError("");
    try {
      const data = await getCurrentWeather(loc || undefined);
      setWeather(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Couldn't load weather for that location.");
      setWeather(null);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    getMyProfile().then((p) => {
      setLocation(p.location || "");
      load(p.location);
    });
  }, []);

  function handleSearch(e) {
    e.preventDefault();
    load(location);
  }

  return (
    <div className="max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-green-400">Weather</h1>
        <p className="text-gray-500 text-sm mt-1">Current conditions and a 7-day outlook.</p>
      </div>

      <form onSubmit={handleSearch} className="flex gap-2">
        <input
          className="flex-1 rounded-lg border border-leaf-100 bg-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-leaf-500"
          placeholder="Search a location…"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
        <button
          type="submit"
          className="rounded-lg bg-green-600 text-white px-4 py-2 font-medium hover:bg-green-700 transition"
        >
          Search
        </button>
      </form>

      {loading && <Spinner label="Loading weather…" />}
      {error && !loading && <ErrorState message={error} onRetry={() => load(location)} />}

      {weather && (
        <>
          <Card>
            <div className="flex items-center gap-8">
              <div>
                <div className="text-5xl font-bold text-green-400">{weather.temperature_c}°C</div>
                <div className="text-sm text-gray-500 mt-1">{weather.location_name}</div>
              </div>
              <div className="text-sm text-gray-400 space-y-1">
                <div>💧 Humidity: {weather.humidity_percent}%</div>
                <div>💨 Wind: {weather.wind_kph} kph</div>
                <div>🌧️ Rain probability: {weather.rain_probability_percent ?? "—"}%</div>
                <div>☔ Rainfall: {weather.rainfall_mm} mm</div>
              </div>
            </div>
            {weather.provider === "mock" && (
              <p className="text-xs text-amber-600 mt-3">
                Showing sample data — connect a WEATHER_API_KEY for live readings.
              </p>
            )}
          </Card>

          {weather.alerts?.length > 0 && (
            <Card title="Alerts" className="border-red-200">
              <ul className="text-sm text-red-700 space-y-1">
                {weather.alerts.map((a) => (
                  <li key={a}>{ALERT_LABELS[a] || a}</li>
                ))}
              </ul>
            </Card>
          )}

          <Card title="7-day forecast">
            <div className="grid grid-cols-3 sm:grid-cols-7 gap-3 text-center">
              {weather.forecast?.map((day) => (
                <div key={day.date} className="text-sm">
                  <div className="text-gray-400 text-xs">
                    {new Date(day.date).toLocaleDateString("en-IN", { weekday: "short" })}
                  </div>
                  <div className="font-medium text-gray-700 mt-1">{day.condition}</div>
                  <div className="text-green-400 font-semibold mt-1">
                    {Math.round(day.temp_max_c)}°
                  </div>
                  <div className="text-gray-400 text-xs">{Math.round(day.temp_min_c)}°</div>
                  <div className="text-xs text-blue-500 mt-1">
                    {day.rain_probability_percent}%
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </>
      )}
    </div>
  );
}
