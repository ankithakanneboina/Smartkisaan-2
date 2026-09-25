import api from "./api";

export async function calculateProfit(payload) {
  const { data } = await api.post("/profit/calculate/", payload);
  return data;
}
