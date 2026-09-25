import api from "./api";

export async function detectDisease(file, cropHint) {
  const form = new FormData();
  form.append("image", file);
  if (cropHint) form.append("crop_hint", cropHint);
  const { data } = await api.post("/diseases/detect/", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function getDiseaseCatalog() {
  const { data } = await api.get("/diseases/");
  return data.results ?? data;
}
