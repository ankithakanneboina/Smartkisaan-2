import api from "./api";

export async function getPosts({ search, category } = {}) {
  const params = {};
  if (search) params.search = search;
  if (category) params.category = category;
  const { data } = await api.get("/community/posts/", { params });
  return data.results ?? data;
}

export async function getPost(id) {
  const { data } = await api.get(`/community/posts/${id}/`);
  return data;
}

export async function createPost(payload) {
  const { data } = await api.post("/community/posts/", payload);
  return data;
}

export async function addComment(postId, content) {
  const { data } = await api.post(`/community/posts/${postId}/comments/`, { content });
  return data;
}

export async function toggleLike(postId) {
  const { data } = await api.post(`/community/posts/${postId}/like/`);
  return data;
}

export async function reportPost(postId, reason) {
  const { data } = await api.post(`/community/posts/${postId}/report/`, { reason });
  return data;
}
