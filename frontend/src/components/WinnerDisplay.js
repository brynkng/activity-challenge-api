import React from "react";
import Typography from "@material-ui/core/Typography";
import withStyles from "@material-ui/core/styles/withStyles";
import Card from "@material-ui/core/Card/Card";

const styles = theme => ({
  winner: {
    background: theme.palette.secondary.light,
    padding: "1em",
    margin: "1em 0"
  }
});
const WinnerDisplay = props => {
  const { classes } = props;

  const text = (
    <span>
      {props.winner.name} is the winner with {props.winner.points} points
    </span>
  );

  return props.large ? (
    <Card className={classes.winner}>
      <Typography variant="h4">{text}</Typography>
    </Card>
  ) : (
    <Typography variant="h5">{text}</Typography>
  );
};

export default withStyles(styles)(WinnerDisplay);
