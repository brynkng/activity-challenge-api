import React from "react";
import { withStyles } from "@material-ui/core/styles";
import {
  getCompetitionData,
  createCompetitionInvitation,
  getCompetitionInvitations
} from "../services/data_provider";
import Button from "@material-ui/core/Button";
import CircularProgress from "@material-ui/core/CircularProgress";
import CompetitionList from "./CompetitionList";
import { Route } from "react-router-dom";
import CompetitionDetail from "./CompetitionDetail";
import CompetitionsContainer from "./CompetitionsContainer";
import CompetitionInvitation from "./CompetitionInvitation";

const styles = theme => ({});

class Dashboard extends React.Component {
  state = {
    fitbit_auth_url: null,
    competitions: null
  };

  handleFitbitAuth = () => {
    window.location = this.state.fitbit_auth_url;
  };

  componentDidMount() {
    this.refreshCompetitions();
  }

  refreshCompetitions = () => {
    getCompetitionData()
      .then(r => {
        if (r.data.authorized) {
          console.log(r.data.data);
          this.setState({ competitions: r.data.data.competitions });
        } else if (r.data.auth_url) {
          if (r.data.errors) {
            this.props.showError(r.data.errors);
          }
          this.setState({ fitbit_auth_url: r.data.auth_url });
        }
      })
      .catch(r => {
        this.props.showError("Server error. Please contact developer.");
        console.log(r.data);

        if (r.response.data.auth_url) {
          this.setState({ fitbit_auth_url: r.response.data.auth_url });
        }
      });
  };

  handleInvite = (competition_id, profile_id, display_name) => {
    createCompetitionInvitation(profile_id, competition_id)
      .then(r => {
        this.updateInviteDisplay(competition_id, profile_id, display_name);
      })
      .catch(r => {
        console.log(r.response.data);
        this.props.showError("Error occurred inviting!");
      });
  };

  updateInviteDisplay = (competition_id, profile_id, display_name) => {
    let competitions = [...this.state.competitions],
      updated = competitions.map(c => {
        if (c.id === competition_id) {
          c.invitable_friends = c.invitable_friends.map(f => {
            if (f.profile_id === profile_id) f.invited = true;
            return f;
          });
        }

        return c;
      });

    this.props.showSuccess(`${display_name} invited!`);

    this.setState({ competitions: updated });
  };

  render() {
    return (
      <>
        {this.state.competitions ? (
          <CompetitionsContainer
            competitions={this.state.competitions}
            handleInvite={this.handleInvite}
            showSuccess={this.props.showSuccess}
            refreshCompetitions={this.refreshCompetitions}
          />
        ) : this.state.fitbit_auth_url ? (
          <Button
            variant="contained"
            color="primary"
            onClick={this.handleFitbitAuth}
          >
            Authorize Fitbit
          </Button>
        ) : (
          <CircularProgress />
        )}
      </>
    );
  }
}

export default withStyles(styles)(Dashboard);
