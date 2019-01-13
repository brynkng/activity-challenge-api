import React from "react";
import { withStyles } from "@material-ui/core";
import Typography from "@material-ui/core/es/Typography/Typography";

const styles = theme => ({
  container: {
    display: "flex",
    margin: "1em 0",
    alignItems: "center"
  },
  avatar: {
    width: "50px",
    height: "50px",
    marginRight: "1em"
  }
});

const FriendInviter = props => {
  const { classes } = props;

  return (
    <div data-fitbit-id={props.friend.encodedId} className={classes.container}>
      <img className={classes.avatar} src={props.friend.avatar} />
      <div className={classes.display_name}>
        <Typography variant="subtitle1">{props.friend.display_name}</Typography>
      </div>
    </div>
  );
};

export default withStyles(styles)(FriendInviter);
