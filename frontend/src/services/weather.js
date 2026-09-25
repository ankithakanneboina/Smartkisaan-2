import api from "./api";

export async function getCurrentWeather(location) {
  const params = location ? { location } : {};
  const { data } = await api.get("/weather/current/", { params });
  return data;
}
