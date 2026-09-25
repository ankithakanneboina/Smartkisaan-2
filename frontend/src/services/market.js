import api from "./api";

export async function getMarketPrices({ crop, market, sort } = {}) {
  const params = {};
  if (crop) params.crop = crop;
  if (market) params.market = market;
  if (sort) params.sort = sort;
  const { data } = await api.get("/market/prices/", { params });
  return data.results ?? data;
}

export async function getMarketTrend(crop, market) {
  const params = { crop };
  if (market) params.market = market;
  const { data } = await api.get("/market/prices/trend/", { params });
  return data;
}
