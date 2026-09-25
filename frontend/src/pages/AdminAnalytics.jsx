import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { useAuth } from "../context/AuthContext";
import { getAnalyticsSummary } from "../services/analytics";
import Card from "../components/Card";

export default function AdminAnalytics() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!user?.is_staff) return;
    getAnalyticsSummary()
      .then(setData)
      .catch(() => setError("Couldn't load analytics."));
  }, [user]);

  if (!user?.is_staff) {
    return (
      <div className="max-w-md">
        <p className="text-sm text-gray-500">This page is only available to administrators.</p>
      </div>
    );
  }

  if (error) return <p className="text-red-600 text-sm">{error}</p>;
  if (!data) return <p className="text-green-500">Loading analytics…</p>;

  return (
    <div className="max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-green-400">Admin Analytics</h1>
        <p className="text-gray-500 text-sm mt-1">Platform usage at a glance.</p>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <Card>
          <div className="text-2xl font-bold text-green-400">{data.total_farmers}</div>
          <div className="text-xs text-gray-500">Total farmers</div>
        </Card>
        <Card>
          <div className="text-2xl font-bold text-green-400">{data.active_farmers_last_30_days}</div>
          <div className="text-xs text-gray-500">Active (30 days)</div>
        </Card>
        <Card>
          <div className="text-2xl font-bold text-green-400">{data.disease_detection_usage.total}</div>
          <div className="text-xs text-gray-500">Disease checks</div>
        </Card>
        <Card>
          <div className="text-2xl font-bold text-green-400">
            {data.recommendation_usage.crop_recommendations + data.recommendation_usage.fertilizer_recommendations}
          </div>
          <div className="text-xs text-gray-500">Recommendations run</div>
        </Card>
      </div>

      <Card title="Most used features">
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={data.most_used_features} layout="vertical" margin={{ left: 20 }}>
            <XAxis type="number" tick={{ fontSize: 11 }} />
            <YAxis type="category" dataKey="feature" tick={{ fontSize: 11 }} width={140} />
            <Tooltip />
            <Bar dataKey="count" fill="#4c9a2a" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </Card>

      {data.popular_crops.length > 0 && (
        <Card title="Popular crops (by farm plans)">
          <ul className="text-sm text-gray-600 space-y-1">
            {data.popular_crops.map((c) => (
              <li key={c.crop} className="flex justify-between">
                <span>{c.crop}</span>
                <span className="text-gray-400">{c.farm_plans} plans</span>
              </li>
            ))}
          </ul>
        </Card>
      )}

      {data.disease_detection_usage.by_status.length > 0 && (
        <Card title="Disease detection status breakdown">
          <ul className="text-sm text-gray-600 space-y-1">
            {data.disease_detection_usage.by_status.map((s) => (
              <li key={s.status} className="flex justify-between">
                <span>{s.status}</span>
                <span className="text-gray-400">{s.count}</span>
              </li>
            ))}
          </ul>
        </Card>
      )}
    </div>
  );
}
