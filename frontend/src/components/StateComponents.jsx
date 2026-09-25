export function Spinner({ label = "Loading…" }) {
  return (
    <div className="flex items-center gap-2 text-green-400 text-sm py-4">
      <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
      </svg>
      {label}
    </div>
  );
}

export function EmptyState({ icon = "📭", title, message, action }) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="text-4xl mb-3">{icon}</div>
      {title && <h3 className="font-semibold text-gray-300 mb-1">{title}</h3>}
      {message && <p className="text-sm text-gray-500 max-w-xs">{message}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}

export function ErrorState({ message, onRetry }) {
  return (
    <div className="flex flex-col items-center justify-center py-10 text-center">
      <div className="text-3xl mb-3">⚠️</div>
      <p className="text-sm text-red-400 mb-3">{message || "Something went wrong."}</p>
      {onRetry && <button onClick={onRetry} className="text-sm text-green-400 underline">Try again</button>}
    </div>
  );
}
