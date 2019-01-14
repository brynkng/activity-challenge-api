import React from "react";
import { withStyles } from "@material-ui/core";
import CompetitionSimple from "./CompetitionSimple";
import Typography from "@material-ui/core/es/Typography/Typography";
import CompetitionInvitation from "./CompetitionInvitation";
import {
  getCompetitionInvitations,
  updateCompetitionInvitation
} from "../services/data_provider";

const styles = theme => ({});

class CompetitionList extends React.Component {
  state = {
    invitations: []
  };

  componentDidMount() {
    console.log("refreshing invitations data");
    getCompetitionInvitations().then(r => {
      if (r.data.invitations) {
        this.setState({ invitations: r.data.invitations });
      }
    });
  }

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

  render() {
    return (
      <>
        {this.props.competitions.length > 0 ? (
          this.props.competitions.map(c => (
            <CompetitionSimple key={c.id} competition={c} />
          ))
        ) : (
          <Typography variant="h6" color="inherit">
            Not participating in any competitions.
          </Typography>
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

export default withStyles(styles)(CompetitionList);
