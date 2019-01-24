import axios from "../axios";

const getCompetitionDetails = competition_id =>
  axios.get(`api/competitions/${competition_id}`);

const getSimpleCompetitionList = () => axios.get("api/competitions/");

const createCompetitionInvitation = (profile_id, competition_id) =>
  axios.post("api/competition_invitations/", {
    profile: profile_id,
    competition: competition_id
  });

const getCompetitionInvitations = () =>
  axios.get("api/competition_invitations/");

const updateCompetitionInvitation = (invitation_id, accepted) =>
  axios.patch(`api/competition_invitations/${invitation_id}`, {
    accepted: accepted
  });

export {
  getCompetitionDetails,
  getSimpleCompetitionList,
  createCompetitionInvitation,
  getCompetitionInvitations,
  updateCompetitionInvitation
};
