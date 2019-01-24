import React from "react";
import { withStyles } from "@material-ui/core";
import CompetitionSimple from "./CompetitionSimple";
import Typography from "@material-ui/core/es/Typography/Typography";
import CompetitionInvitation from "./CompetitionInvitation";
import {
  createCompetitionInvitation,
  getCompetitionInvitations,
  getSimpleCompetitionList,
  updateCompetitionInvitation
} from "../services/data_provider";
import { withRouter } from "react-router";
import CircularProgress from "@material-ui/core/CircularProgress";

const styles = theme => ({});

class CompetitionList extends React.Component {
  state = {
    invitations: [],
    competitions: null
  };

  componentDidMount() {
    this.refreshCompetitions();

    getCompetitionInvitations().then(r => {
      if (r.data.invitations) {
        this.setState({ invitations: r.data.invitations });
      }
    });
  }

  refreshCompetitions = () => {
    getSimpleCompetitionList()
      .then(r => {
        if (r.data.authorized) {
          this.setState({ competitions: r.data.data.competitions });
        } else if (r.data.auth_url) {
          if (r.data.errors) {
            this.props.showError(r.data.errors);
          }

          this.authRedirect(r.data.auth_url);
        }
      })
      .catch(r => {
        this.props.showError("Server error. Please contact developer.");
        console.log(r.data);
      });
  };

  authRedirect = url => {
    this.props.history.replace(`/fitbit_auth/?url=${encodeURIComponent(url)}`);
  };

  handleAccept = id => {
    this.removeInvitation(id);

    updateCompetitionInvitation(id, true).then(r => {
      this.props.showSuccess("Invitation accepted!");
      this.props.refreshCompetitions();
    });
  };

  handleReject = id => {
    this.removeInvitation(id);
    updateCompetitionInvitation(id, false).then();
  };

  removeInvitation = id => {
    let invitations = [...this.state.invitations],
      updated = invitations.filter(i => i.id !== id);
    this.setState({ invitations: updated });
  };

  render_simple_competitions = (label, competitions) => {
    return competitions.length > 0 ? (
      <>
        <Typography variant="h5">{label}</Typography>
        {competitions.map(c => (
          <CompetitionSimple key={c.id} competition={c} />
        ))}
      </>
    ) : null;
  };

  render() {
    let current_competitions,
      past_competitions = [];

    if (this.state.competitions) {
      current_competitions = this.state.competitions.filter(c => c.current);
      past_competitions = this.state.competitions.filter(c => !c.current);
    }

    return (
      <>
        {this.state.competitions ? (
          <>
            {this.render_simple_competitions("Current", current_competitions)}
            {this.render_simple_competitions("Past", past_competitions)}

            {current_competitions.length === 0 &&
            past_competitions.length === 0 ? (
              <Typography variant="h5" color="inherit">
                Not participating in any competitions.
              </Typography>
            ) : null}
          </>
        ) : (
          <CircularProgress />
        )}

        {this.state.invitations.map(i => (
          <CompetitionInvitation
            key={i.id}
            invitation={i}
            handleAccept={this.handleAccept}
            handleReject={this.handleReject}
          />
        ))}
      </>
    );
  }
}

export default withStyles(styles)(withRouter(CompetitionList));
