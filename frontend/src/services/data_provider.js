import axios from "../axios";

function getFitbitData() {
  return axios.get("api/fitbit_data/")
}

function getCompetitionFriendList(competition_id) {
  return axios.get(`api/competition_friend_list/${competition_id}`);
}

export { getFitbitData, getCompetitionFriendList };
