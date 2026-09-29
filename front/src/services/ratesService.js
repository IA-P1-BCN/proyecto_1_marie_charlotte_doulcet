import client from "./apiClient.js";

export const getRates = () => client.get("/rates").then(({ data }) => data);
export const saveRates = (rates) => client.put("/rates", rates);
