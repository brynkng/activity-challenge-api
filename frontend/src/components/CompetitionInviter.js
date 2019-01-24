import React from "react";
import { withStyles, withWidth } from "@material-ui/core";
import Typography from "@material-ui/core/es/Typography/Typography";
import CircularProgress from "@material-ui/core/es/CircularProgress/CircularProgress";
import FriendInviter from "./FriendInviter";
import Card from "@material-ui/core/Card";
import { isWidthUp } from "@material-ui/core/withWidth";

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
        <FriendInviter
          key={f.profile_id}
          friend={f}
          handleInvite={props.handleInvite}
          competition_id={competition.id}
        />
      ))
    : null;

  return (
    <Card
      className={classes.container}
      elevation={0}
      // elevation={isWidthUp("sm", props.width) ? 1 : 0}
    >
      <Typography variant="h6">Invite Friends</Typography>

      {invitable_friends ? <>{invitable_friends}</> : <CircularProgress />}
    </Card>
  );
};

export default withStyles(styles)(withWidth()(CompetitionInviter));
