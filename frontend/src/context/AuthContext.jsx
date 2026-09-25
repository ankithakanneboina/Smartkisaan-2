import { createContext, useContext, useEffect, useState } from "react";
import { getTokens } from "../services/api";
import * as authApi from "../services/auth";

const AuthContext = createContext(null);

export function roleHomePath(user) {
  if (!user) return "/login";
  if (user.role === "admin" || user.is_staff) return "/admin/dashboard";
  if (user.role === "farmer") return "/farmer/dashboard";
  return "/dashboard";
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const { access } = getTokens();
    if (!access) { setLoading(false); return; }
    authApi.fetchMe().then(setUser).catch(() => setUser(null)).finally(() => setLoading(false));
  }, []);

  const value = {
    user, loading,
    isAuthenticated: !!user,
    isAdmin: !!(user?.role === "admin" || user?.is_staff),
    isFarmer: user?.role === "farmer",
    isBuyer: user?.role === "buyer",
    async login(email, password) { const me = await authApi.login(email, password); setUser(me); return me; },
    async register(payload) { const me = await authApi.register(payload); setUser(me); return me; },
    async logout() { await authApi.logout(); setUser(null); },
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
