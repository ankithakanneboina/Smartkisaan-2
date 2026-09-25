import { Navigate } from "react-router-dom";
import { useAuth, roleHomePath } from "../context/AuthContext";

export default function ProtectedRoute({ children, role }) {
  const { user, loading, isAuthenticated, isAdmin, isFarmer, isBuyer } = useAuth();
  if (loading) return <div className="min-h-screen flex items-center justify-center text-leaf-600">Loading…</div>;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (role === "admin" && !isAdmin) return <Navigate to={roleHomePath(user)} replace />;
  if (role === "farmer" && !isFarmer && !isAdmin) return <Navigate to={roleHomePath(user)} replace />;
  if (role === "buyer" && !isBuyer && !isAdmin) return <Navigate to={roleHomePath(user)} replace />;
  return children;
}
