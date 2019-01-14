import React from "react";
import Card from "@material-ui/core/es/Card/Card";
import Typography from "@material-ui/core/es/Typography/Typography";
import withStyles from "@material-ui/core/styles/withStyles";
import CheckIcon from "@material-ui/icons/Check";
import RejectIcon from "@material-ui/icons/Cancel";
import moment from "moment";

const styles = theme => ({
  container: {
    padding: "1em",
    margin: "1em 0",
    color: theme.palette.secondary.contrastText,
    background: theme.palette.secondary.main
  },
  controls: {
    marginTop: "1em",
    display: "flex",
    justifyContent: "space-evenly"
  },
  icon: {
    "&:hover": {
      cursor: "pointer",
      color: theme.palette.secondary.light,
      transition: ".3s color"
    }
  }
});

const CompetitionInvitation = props => {
  const { classes } = props;

  return (
    <Card className={classes.container}>
      <Typography variant="button" color="inherit">
        {props.invitation.sender.user.username} invited you to{" "}
        {props.invitation.competition.name} starting{" "}
        {moment(props.invitation.competition.start).format("MMMM Do")}
      </Typography>
      <div className={classes.controls}>
        <RejectIcon
          className={classes.icon}
          fontSize="large"
          onClick={() => props.handleReject(props.invitation.id)}
        />
        <CheckIcon
          className={classes.icon}
          fontSize="large"
          onClick={() => props.handleAccept(props.invitation.id)}
        />
      </div>
    </Card>
  );
};

export default withStyles(styles)(CompetitionInvitation);
