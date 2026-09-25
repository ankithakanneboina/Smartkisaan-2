import api from "./api";

export async function getAnalyticsSummary() {
  const { data } = await api.get("/analytics/summary/");
  return data;
}
