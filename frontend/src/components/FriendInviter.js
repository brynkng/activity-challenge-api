import React from "react";
import { withStyles } from "@material-ui/core";
import Typography from "@material-ui/core/es/Typography/Typography";
import AddIcon from "@material-ui/icons/AddBox";
import classNames from "classnames";

const styles = theme => ({
  container: {
    display: "flex",
    margin: "1em 0",
    alignItems: "center",
    cursor: "pointer",
    transition: ".3s color",
    "&:hover": {
      color: theme.palette.secondary.light
    }
  },
  avatar: {
    width: "50px",
    height: "50px",
    marginRight: "1em"
  },
  display_name: {
    marginRight: ".5em"
  },
  disabled: {
    opacity: ".3",
    "&:hover": {
      color: "inherit"
    }
  }
});

const FriendInviter = props => {
  const { classes } = props,
    handleInvite = () => {
      if (!props.friend.invited) {
        props.handleInvite(
          props.competition_id,
          props.friend.profile_id,
          props.friend.display_name
        );
      }
    };

  return (
    <div
      onClick={handleInvite}
      className={classNames(classes.container, {
        [classes.disabled]: props.friend.invited
      })}
    >
      <img className={classes.avatar} src={props.friend.avatar} />
      <div className={classes.display_name}>
        <Typography variant="subtitle1">{props.friend.display_name}</Typography>
      </div>
      <AddIcon />
    </div>
  );
};

export default withStyles(styles)(FriendInviter);
