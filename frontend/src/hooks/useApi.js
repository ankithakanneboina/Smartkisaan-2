import { useState, useCallback } from "react";

/**
 * Wraps an async API call with loading/error/data state so every page
 * doesn't hand-roll the same try/catch/finally pattern. Also normalizes
 * the error message from our custom exception handler's { detail: "..." }
 * shape, Axios network errors, and plain JS Error objects.
 *
 * Usage:
 *   const { data, loading, error, run } = useApi(fetchSomething);
 *   useEffect(() => { run(arg1, arg2); }, []);
 */
export function useApi(fn) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const run = useCallback(async (...args) => {
    setLoading(true);
    setError("");
    try {
      const result = await fn(...args);
      setData(result);
      return result;
    } catch (err) {
      const msg = extractErrorMessage(err);
      setError(msg);
      throw err; // re-throw so the caller can handle it too if needed
    } finally {
      setLoading(false);
    }
  }, [fn]);

  return { data, loading, error, run, setData };
}

export function extractErrorMessage(err) {
  // Our custom exception handler sends { detail: "..." }
  if (err?.response?.data?.detail) return err.response.data.detail;
  // Axios network/timeout errors
  if (err?.message === "Network Error") return "Network error — check your connection.";
  if (err?.code === "ECONNABORTED") return "Request timed out — please try again.";
  // Fallback
  return err?.message || "Something went wrong.";
}
