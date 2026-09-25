import api from "./api";

export async function sendChatMessage(message, language) {
  const { data } = await api.post("/ai/chat/", { message, language });
  return data;
}

export async function getChatHistory() {
  const { data } = await api.get("/ai/history/");
  return data.results ?? data;
}
