import api from "./api";

export async function recommendCrops(payload) {
  const { data } = await api.post("/crops/recommend/", payload);
  return data;
}
