import { useTheme } from "../context/ThemeContext";

export default function ThemeToggle() {
  const { dark, toggle } = useTheme();
  return (
    <button
      onClick={toggle}
      title={dark ? "Switch to light mode" : "Switch to dark mode"}
      className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition
        bg-gray-700 text-gray-200 hover:bg-gray-600 dark:bg-gray-700 dark:text-gray-200"
    >
      {dark ? "☀️ Light" : "🌙 Dark"}
    </button>
  );
}
