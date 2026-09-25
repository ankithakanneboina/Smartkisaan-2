import api from "./api";
export async function sendOtp(phone_number) { const { data } = await api.post("/auth/otp/send/", { phone_number }); return data; }
export async function verifyOtp(session_id, otp) { const { data } = await api.post("/auth/otp/verify/", { session_id, otp }); return data; }
