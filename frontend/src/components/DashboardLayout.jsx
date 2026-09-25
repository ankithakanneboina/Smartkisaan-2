import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth, roleHomePath } from "../context/AuthContext";
import ThemeToggle from "./ThemeToggle";

const SHARED = [
  { to: "/weather", label: "Weather", icon: "⛅" },
  { to: "/market", label: "Market", icon: "📈" },
  { to: "/assistant", label: "AI Assistant", icon: "💬" },
  { to: "/schemes", label: "Schemes", icon: "📜" },
  { to: "/videos", label: "Videos", icon: "🎬" },
  { to: "/community", label: "Community", icon: "👥" },
  { to: "/profile", label: "My Profile", icon: "👤" },
];

const NAV = {
  buyer: [
    { to: "/dashboard", label: "Dashboard", icon: "🏠" },
    { to: "/marketplace", label: "Marketplace", icon: "🛒" },
    { to: "/diseases/detect", label: "Disease", icon: "🔬" },
    ...SHARED,
  ],
  farmer: [
    { to: "/farmer/dashboard", label: "Dashboard", icon: "🏠" },
    { to: "/crops/recommend", label: "Crops", icon: "🌾" },
    { to: "/fertilizers/recommend", label: "Fertilizer", icon: "🧪" },
    { to: "/farm-plan", label: "Farm Plan", icon: "📅" },
    { to: "/profit", label: "Profit", icon: "💰" },
    { to: "/marketplace", label: "Marketplace", icon: "🛒" },
    { to: "/diseases/detect", label: "Disease", icon: "🔬" },
    ...SHARED,
  ],
  admin: [
    { to: "/admin/dashboard", label: "Dashboard", icon: "📊" },
    { to: "/admin/users", label: "Users", icon: "👥" },
    { to: "/admin/analytics", label: "Analytics", icon: "📈" },
    { to: "/marketplace", label: "Marketplace", icon: "🛒" },
    ...SHARED,
  ],
};

const BADGE = {
  admin: "bg-red-900 text-red-300",
  farmer: "bg-green-900 text-green-300",
  buyer: "bg-blue-900 text-blue-300",
};

export default function DashboardLayout() {
  const { user, logout, isAdmin, isFarmer } = useAuth();
  const navigate = useNavigate();
  const role = isAdmin ? "admin" : isFarmer ? "farmer" : "buyer";
  const navItems = NAV[role];

  async function handleLogout() { await logout(); navigate("/login"); }

  return (
    <div className="min-h-screen flex bg-gray-900">
      {/* Sidebar */}
      <aside className="hidden md:flex md:flex-col w-56 bg-gray-800 border-r border-gray-700 p-4">
        <div className="mb-4">
          <div className="text-xl font-bold text-green-400">🌾 Smart Kisaan</div>
          <span className={`text-xs px-2 py-0.5 rounded-full font-medium mt-1 inline-block ${BADGE[role]}`}>
            {role}
          </span>
        </div>

        <nav className="flex-1 space-y-0.5 overflow-y-auto">
          {navItems.map(item => (
            <NavLink key={item.to} to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition
                ${isActive
                  ? "bg-green-900 text-green-300"
                  : "text-gray-400 hover:bg-gray-700 hover:text-gray-100"}`
              }>
              <span>{item.icon}</span>{item.label}
            </NavLink>
          ))}
        </nav>

        <div className="mt-4 space-y-2">
          <ThemeToggle />
          <button onClick={handleLogout}
            className="w-full text-sm text-left px-3 py-2 rounded-lg text-red-400 hover:bg-red-900 hover:text-red-300 transition">
            🚪 Log out
          </button>
        </div>
      </aside>

      {/* Main */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Mobile header */}
        <header className="md:hidden flex items-center justify-between bg-gray-800 border-b border-gray-700 px-4 py-3">
          <span className="font-bold text-green-400">🌾 Smart Kisaan</span>
          <div className="flex items-center gap-2">
            <ThemeToggle />
            <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${BADGE[role]}`}>{role}</span>
            <button onClick={handleLogout} className="text-sm text-red-400">Out</button>
          </div>
        </header>

        {/* Desktop topbar */}
        <header className="hidden md:flex items-center justify-between bg-gray-800 border-b border-gray-700 px-6 py-3">
          <span className="text-sm text-gray-400">
            {new Date().toLocaleDateString("en-IN", { weekday: "long", day: "numeric", month: "long" })}
          </span>
          <span className="text-sm font-medium text-gray-300">{user?.email}</span>
        </header>

        <main className="flex-1 p-4 md:p-6 bg-gray-900">
          <Outlet />
        </main>

        {/* Mobile bottom nav */}
        <nav className="md:hidden flex justify-around bg-gray-800 border-t border-gray-700 py-2">
          {navItems.slice(0, 5).map(item => (
            <NavLink key={item.to} to={item.to}
              className={({ isActive }) =>
                `text-xs flex flex-col items-center gap-0.5 ${isActive ? "text-green-400" : "text-gray-500"}`
              }>
              <span className="text-lg">{item.icon}</span>
              {item.label.split(" ")[0]}
            </NavLink>
          ))}
        </nav>
      </div>
    </div>
  );
}
