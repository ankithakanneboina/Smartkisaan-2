export default function FormField({ label, error, children }) {
  return (
    <label className="block mb-4">
      <span className="block text-sm font-medium text-gray-300 mb-1">{label}</span>
      {children}
      {error && <span className="block text-sm text-red-400 mt-1">{error}</span>}
    </label>
  );
}
