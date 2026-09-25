import api from "./api";

export async function recommendFertilizers(payload) {
  const { data } = await api.post("/fertilizers/recommend/", payload);
  return data;
}
