import { useEffect, useState } from "react";
import api from "../services/api";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import Card from "../components/Card";

export default function AdminDashboard() {
  const [data, setData] = useState(null);
  useEffect(() => { api.get("/admin/analytics/").then(r => setData(r.data)).catch(() => {}); }, []);
  const roleChart = data?.totalUsersByRole ? Object.entries(data.totalUsersByRole).map(([role,count]) => ({ role, count })) : [];
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-green-400">📊 Admin Dashboard</h1>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {[["Farmers",data?.totalUsersByRole?.farmer??"—"],["Active Users",data?.activeUsers??"—"],["Total Logins",data?.totalLogins??"—"],["Today Logins",data?.todayLogins??"—"]].map(([label,value]) => (
          <Card key={label}><div className="text-2xl font-bold text-green-400">{value}</div><div className="text-xs text-gray-500 mt-1">{label}</div></Card>
        ))}
      </div>
      {roleChart.length > 0 && (
        <Card title="Users by role">
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={roleChart}>
              <XAxis dataKey="role" tick={{ fontSize:12, fill:"#9ca3af" }} />
              <YAxis tick={{ fontSize:11, fill:"#9ca3af" }} />
              <Tooltip contentStyle={{ backgroundColor:"#1f2937", border:"1px solid #374151", color:"#f3f4f6" }} />
              <Bar dataKey="count" fill="#16a34a" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      )}
      <Card title="Admin tools">
        <div className="flex flex-wrap gap-3 text-sm">
          <a href="/admin/users" className="text-green-400 hover:underline">👥 Manage users</a>
          <a href="/admin/analytics" className="text-green-400 hover:underline">📈 Full analytics</a>
          <a href="/community" className="text-green-400 hover:underline">💬 Community</a>
        </div>
      </Card>
    </div>
  );
}
