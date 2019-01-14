import axios from "../axios";

function getCompetitionData() {
  return axios.get("api/fitbit_data/");
}

function createCompetitionInvitation(profile_id, competition_id) {
  return axios.post("api/competition_invitations/", {
    profile: profile_id,
    competition: competition_id
  });
}

function getCompetitionInvitations() {
  return axios.get("api/competition_invitations/");
}

function updateCompetitionInvitation(invitation_id, accepted) {
  return axios.patch(`api/competition_invitations/${invitation_id}`, {
    accepted: accepted
  });
}

export {
  getCompetitionData,
  createCompetitionInvitation,
  getCompetitionInvitations,
  updateCompetitionInvitation
};
