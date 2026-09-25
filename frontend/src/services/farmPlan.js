import api from "./api";

export async function getCropCalendar(crop) {
  const { data } = await api.get("/farm-plan/calendar/", { params: { crop } });
  return data.results ?? data;
}

export async function generateFarmPlan(payload) {
  const { data } = await api.post("/farm-plan/generate/", payload);
  return data;
}

export async function getFarmPlans() {
  const { data } = await api.get("/farm-plan/plans/");
  return data.results ?? data;
}

export async function updatePlanStatus(id, status) {
  const { data } = await api.patch(`/farm-plan/plans/${id}/`, { status });
  return data;
}

export async function updateTask(id, payload) {
  const { data } = await api.patch(`/farm-plan/tasks/${id}/`, payload);
  return data;
}
