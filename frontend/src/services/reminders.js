import api from "./api";

export async function getUpcomingReminders() {
  const { data } = await api.get("/reminders/upcoming/");
  return data.results ?? data;
}

export async function createReminder(payload) {
  const { data } = await api.post("/reminders/", payload);
  return data;
}

export async function markReminderDone(id) {
  const { data } = await api.patch(`/reminders/${id}/`, { is_done: true });
  return data;
}

export async function getNotificationPreferences() {
  const { data } = await api.get("/reminders/preferences/");
  return data;
}

export async function updateNotificationPreferences(payload) {
  const { data } = await api.patch("/reminders/preferences/", payload);
  return data;
}
