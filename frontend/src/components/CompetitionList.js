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
import { Redirect, withRouter } from "react-router";
import CircularProgress from "@material-ui/core/CircularProgress";
import Divider from "@material-ui/core/Divider";

const styles = theme => ({
  divider: {
    margin: "0.3em 0 2em 0"
  }
});

class CompetitionList extends React.Component {
  state = {
    invitations: [],
    competitions: null,
    auth_url: null
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

          // this.authRedirect(r.data.auth_url);
          this.setState({ auth_url: r.data.auth_url });
        }
      })
      .catch(r => {
        this.props.showError("Server error. Please contact developer.");
        console.log(r.data);
      });
  };

  authRedirect = url => {
    this.props.history.push(`/fitbit_auth/?url=${encodeURIComponent(url)}`);
  };

  handleAccept = id => {
    this.removeInvitation(id);

    updateCompetitionInvitation(id, true).then(r => {
      this.props.showSuccess("Invitation accepted!");
      this.refreshCompetitions();
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
    const { classes } = this.props;

    return competitions.length > 0 ? (
      <>
        <Typography variant="h4">{label}</Typography>
        <Divider className={classes.divider} />
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
        {this.state.auth_url ? (
          <Redirect
            to={{
              pathname: "/fitbit_auth",
              state: { auth_url: this.state.auth_url }
            }}
          />
        ) : null}

        {this.state.competitions ? (
          <>
            {this.render_simple_competitions("Current", current_competitions)}
            {this.render_simple_competitions("Completed", past_competitions)}

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
