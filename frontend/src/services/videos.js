import api from "./api";

export async function getVideos({ search, category } = {}) {
  const params = {};
  if (search) params.search = search;
  if (category) params.category = category;
  const { data } = await api.get("/videos/", { params });
  return data.results ?? data;
}

export async function toggleFavorite(id) {
  const { data } = await api.post(`/videos/${id}/favorite/`);
  return data;
}

export async function logWatch(id) {
  await api.post(`/videos/${id}/watch/`);
}

export async function getFavoriteVideos() {
  const { data } = await api.get("/videos/favorites/");
  return data.results ?? data;
}
