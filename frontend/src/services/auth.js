import api, { setTokens, clearTokens, getTokens } from "./api";

export async function register(payload) {
  const { data } = await api.post("/auth/register/", payload);
  setTokens({ access: data.access, refresh: data.refresh });
  return data.user;
}

export async function login(email, password) {
  const { data } = await api.post("/auth/login/", { email, password });
  setTokens({ access: data.access, refresh: data.refresh });
  return fetchMe();
}

export async function fetchMe() {
  const { data } = await api.get("/auth/me/");
  return data;
}

export async function logout() {
  const { refresh } = getTokens();
  try {
    if (refresh) await api.post("/auth/logout/", { refresh });
  } finally {
    clearTokens();
  }
}
