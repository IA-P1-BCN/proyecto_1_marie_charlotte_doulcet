import client from "./apiClient.js";

const data = ({ data: body }) => body;

export const getActiveRide = () => client.get("/ride").then(data);
export const startRide = (rates) => client.post("/ride/start", rates).then(data);
export const changeRideState = (state) => client.patch("/ride/state", { state }).then(data);
export const endRide = () => client.post("/ride/end").then(data);
export const getTodayRides = () => client.get("/rides").then(data);
