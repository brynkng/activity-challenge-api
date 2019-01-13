import axios from "../axios";

function getFitbitData() {
  return axios.get("api/fitbit_data/")
}

export { getFitbitData };
