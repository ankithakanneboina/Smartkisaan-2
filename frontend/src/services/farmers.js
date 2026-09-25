import api from "./api";

export async function getMyProfile() {
  const { data } = await api.get("/farmers/me/");
  return data;
}

export async function updateMyProfile(payload) {
  const { data } = await api.patch("/farmers/me/", payload);
  return data;
}

// Separate call because it needs multipart/form-data, unlike the
// plain-JSON PATCH above.
export async function uploadProfilePhoto(file) {
  const form = new FormData();
  form.append("profile_photo", file);
  const { data } = await api.patch("/farmers/me/", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}
