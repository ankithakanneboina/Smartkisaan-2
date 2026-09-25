import { useAuth } from "../context/AuthContext";
import Card from "../components/Card";

export default function FarmerDashboard() {
  const { user } = useAuth();
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-green-400">🌾 Farmer Dashboard</h1>
        <p className="text-gray-500 text-sm mt-1">Welcome, {user?.username}</p>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Card title="Farm tools">
          <div className="flex flex-col gap-2 text-sm">
            <a href="/crops/recommend" className="text-green-400 hover:underline">🌾 Crop recommendation</a>
            <a href="/fertilizers/recommend" className="text-green-400 hover:underline">🧪 Fertilizer advice</a>
            <a href="/farm-plan" className="text-green-400 hover:underline">📅 Farm plan</a>
            <a href="/profit" className="text-green-400 hover:underline">💰 Profit calculator</a>
            <a href="/diseases/detect" className="text-green-400 hover:underline">🔬 Disease detection</a>
          </div>
        </Card>
        <Card title="Sell & Market">
          <div className="flex flex-col gap-2 text-sm">
            <a href="/marketplace" className="text-green-400 hover:underline">🛒 Marketplace</a>
            <a href="/market" className="text-green-400 hover:underline">📈 Market prices</a>
            <a href="/assistant" className="text-green-400 hover:underline">💬 AI assistant</a>
            <a href="/community" className="text-green-400 hover:underline">👥 Community</a>
          </div>
        </Card>
      </div>
    </div>
  );
}
