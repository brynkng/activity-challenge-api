import React from "react";
import { withStyles } from "@material-ui/core";
import Typography from "@material-ui/core/es/Typography/Typography";
import CircularProgress from "@material-ui/core/es/CircularProgress/CircularProgress";
import FriendInviter from "./FriendInviter";
import Card from "@material-ui/core/Card";

const styles = theme => ({
  container: {
    padding: "1.5em"
  }
});

const CompetitionInviter = props => {
  const { classes } = props,
    competition = props.competition;

  let invitable_friends = competition.invitable_friends
    ? competition.invitable_friends.map(f => (
        <FriendInviter key={f.profile_id} friend={f} />
      ))
    : null;

  return (
    <Card className={classes.container}>
      <Typography variant="subheading">Invite Friends</Typography>

      {invitable_friends ? <>{invitable_friends}</> : <CircularProgress />}
    </Card>
  );
};

export default withStyles(styles)(CompetitionInviter);
