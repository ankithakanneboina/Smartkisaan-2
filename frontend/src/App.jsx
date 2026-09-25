import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth, roleHomePath } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import DashboardLayout from "./components/DashboardLayout";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import FarmerDashboard from "./pages/FarmerDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import AdminUsers from "./pages/AdminUsers";
import Profile from "./pages/Profile";
import CropRecommendation from "./pages/CropRecommendation";
import FertilizerRecommendation from "./pages/FertilizerRecommendation";
import Weather from "./pages/Weather";
import MarketPrices from "./pages/MarketPrices";
import ProfitCalculator from "./pages/ProfitCalculator";
import DiseaseDetection from "./pages/DiseaseDetection";
import DiseaseReference from "./pages/DiseaseReference";
import AIAssistant from "./pages/AIAssistant";
import FarmPlan from "./pages/FarmPlan";
import Schemes from "./pages/Schemes";
import Videos from "./pages/Videos";
import Marketplace from "./pages/Marketplace";
import Community from "./pages/Community";
import CommunityPostDetail from "./pages/CommunityPostDetail";
import AdminAnalytics from "./pages/AdminAnalytics";

function RootRedirect() {
  const { user, loading } = useAuth();
  if (loading) return null;
  return <Navigate to={roleHomePath(user)} replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route element={<ProtectedRoute><DashboardLayout /></ProtectedRoute>}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/farmer/dashboard" element={<ProtectedRoute role="farmer"><FarmerDashboard /></ProtectedRoute>} />
            <Route path="/admin/dashboard" element={<ProtectedRoute role="admin"><AdminDashboard /></ProtectedRoute>} />
            <Route path="/admin/users" element={<ProtectedRoute role="admin"><AdminUsers /></ProtectedRoute>} />
            <Route path="/admin/analytics" element={<ProtectedRoute role="admin"><AdminAnalytics /></ProtectedRoute>} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/weather" element={<Weather />} />
            <Route path="/market" element={<MarketPrices />} />
            <Route path="/assistant" element={<AIAssistant />} />
            <Route path="/schemes" element={<Schemes />} />
            <Route path="/videos" element={<Videos />} />
            <Route path="/community" element={<Community />} />
            <Route path="/community/:id" element={<CommunityPostDetail />} />
            <Route path="/diseases/detect" element={<DiseaseDetection />} />
            <Route path="/diseases/reference" element={<DiseaseReference />} />
            <Route path="/crops/recommend" element={<CropRecommendation />} />
            <Route path="/fertilizers/recommend" element={<FertilizerRecommendation />} />
            <Route path="/profit" element={<ProfitCalculator />} />
            <Route path="/farm-plan" element={<FarmPlan />} />
            <Route path="/marketplace" element={<Marketplace />} />
          </Route>
          <Route path="/" element={<RootRedirect />} />
          <Route path="*" element={<RootRedirect />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
