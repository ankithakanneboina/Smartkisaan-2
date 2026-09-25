import api from "./api";

export async function getRecentActivities() {
  const { data } = await api.get("/farm-activities/recent/");
  return data.results ?? data;
}

export async function createActivity(payload) {
  const { data } = await api.post("/farm-activities/", payload);
  return data;
}
