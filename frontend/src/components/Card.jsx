export default function Card({ title, children, className = "" }) {
  return (
    <div className={`bg-gray-800 rounded-2xl border border-gray-700 shadow-sm p-5 ${className}`}>
      {title && <h2 className="text-sm font-semibold text-green-400 mb-3">{title}</h2>}
      {children}
    </div>
  );
}
