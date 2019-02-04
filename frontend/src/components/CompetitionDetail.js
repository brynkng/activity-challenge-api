import React, { Component } from "react";
import { withStyles } from "@material-ui/core";
import Typography from "@material-ui/core/Typography";
import { withRouter } from "react-router";
import CompetitionInviter from "./CompetitionInviter";
import Grid from "@material-ui/core/Grid";
import PointDisplay from "./PointDisplay";
import ArrowBackIcon from "@material-ui/icons/ArrowBack";
import { Link } from "react-router-dom";
import {
  createCompetitionInvitation,
  getCompetitionDetails
} from "../services/data_provider";
import CircularProgress from "@material-ui/core/CircularProgress";
import WinnerDisplay from "./WinnerDisplay";
import moment from "moment";

const styles = theme => ({
  title: {
    margin: ".5em 0"
  },
  card: {
    padding: "1.5em 0"
  },
  table: {
    marginTop: "1em"
  },
  headerContainer: {
    position: "relative"
  },
  backLink: {
    position: "absolute",
    left: 0,
    color: "inherit"
  }
});

class CompetitionDetail extends Component {
  state = {
    competition: null
  };

  componentDidMount() {
    const id = parseInt(this.props.match.params.id);
    getCompetitionDetails(id)
      .then(r => {
        this.setState({ competition: r.data.data });
      })
      .catch(r => {
        console.log(r);
        this.props.showError("Error loading competition details");
      });
  }

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
    let competition = { ...this.state.competition };

    competition.invitable_friends = competition.invitable_friends.map(f => {
      if (f.profile_id === profile_id) f.invited = true;
      return f;
    });

    this.props.showSuccess(`${display_name} invited!`);

    this.setState({ competition: competition });
  };

  render() {
    const { classes } = this.props;
    const invitable_friends =
      this.state.competition &&
      this.state.competition.current &&
      this.state.competition.invitable_friends.length > 0;

    return this.state.competition ? (
      <>
        <header className={classes.headerContainer}>
          <Link to="/" className={classes.backLink}>
            <ArrowBackIcon fontSize="large" />
          </Link>
          <Typography variant="display1" className={classes.title}>
            {this.state.competition.name}
          </Typography>
          <Typography variant="h5">
            {moment(this.state.competition.start).format("MMMM D")} -{" "}
            {moment(this.state.competition.end).format("D")}
          </Typography>
        </header>

        <WinnerDisplay winner={this.state.competition.winner} large />

        <Grid container spacing={24} justify="center">
          <Grid item xs={12} md={4}>
            <PointDisplay
              name={"Me"}
              point_details={this.state.competition.point_details}
            />
          </Grid>

          {this.state.competition.competition_members.map(m => (
            <Grid item xs={12} md={4} key={m.profile_id}>
              <PointDisplay name={m.display_name} point_details={m} />
            </Grid>
          ))}
        </Grid>
        {invitable_friends ? (
          <Grid container spacing={24} justify="center">
            <Grid item xs={12} md={6}>
              <CompetitionInviter
                competition={this.state.competition}
                handleInvite={this.handleInvite}
              />
            </Grid>
          </Grid>
        ) : null}
      </>
    ) : (
      <CircularProgress />
    );
  }
}

export default withRouter(withStyles(styles)(CompetitionDetail));
