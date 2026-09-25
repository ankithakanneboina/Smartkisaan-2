import api from "./api";

export async function getSchemes({ search, category } = {}) {
  const params = {};
  if (search) params.search = search;
  if (category) params.category = category;
  const { data } = await api.get("/schemes/", { params });
  return data.results ?? data;
}
