import api from "./api";

export async function getProducts({ search, category } = {}) {
  const params = {};
  if (search) params.search = search;
  if (category) params.category = category;
  const { data } = await api.get("/marketplace/products/", { params });
  return data.results ?? data;
}

export async function toggleWishlist(id) {
  const { data } = await api.post(`/marketplace/products/${id}/wishlist/`);
  return data;
}

export async function getWishlist() {
  const { data } = await api.get("/marketplace/wishlist/");
  return data.results ?? data;
}
