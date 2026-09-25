import axios from "axios";

// Every later phase's API modules (crops.js, weather.js, ai.js, ...) import
// this same instance so auth headers and refresh logic are handled once.
const api = axios.create({ baseURL: "/api" });

export function getTokens() {
  return {
    access: localStorage.getItem("sk_access"),
    refresh: localStorage.getItem("sk_refresh"),
  };
}

export function setTokens({ access, refresh }) {
  if (access) localStorage.setItem("sk_access", access);
  if (refresh) localStorage.setItem("sk_refresh", refresh);
}

export function clearTokens() {
  localStorage.removeItem("sk_access");
  localStorage.removeItem("sk_refresh");
}

api.interceptors.request.use((config) => {
  const { access } = getTokens();
  if (access) config.headers.Authorization = `Bearer ${access}`;
  return config;
});

// On a 401, try exactly one silent refresh before giving up — avoids
// bouncing the user to the login page on every access-token expiry.
let refreshingPromise = null;

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retried) {
      original._retried = true;
      const { refresh } = getTokens();
      if (!refresh) return Promise.reject(error);

      try {
        refreshingPromise =
          refreshingPromise ||
          axios.post("/api/auth/refresh/", { refresh }).finally(() => {
            refreshingPromise = null;
          });
        const { data } = await refreshingPromise;
        setTokens({ access: data.access });
        original.headers.Authorization = `Bearer ${data.access}`;
        return api(original);
      } catch (refreshError) {
        clearTokens();
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default api;
