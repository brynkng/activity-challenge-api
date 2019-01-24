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

  const calculateWinner = () => {
    let my_point_details = {
      display_name: "Me",
      ...props.competition.point_details
    };

    let all_point_details = [
      my_point_details,
      ...props.competition.competition_members
    ];

    return all_point_details.sort((a, b) => a.points - b.points)[0];
  };

  let winner =
    props.competition && !props.competition.current ? calculateWinner() : null;

  return winner ? (
    <Card className={classes.winner}>
      <Typography variant="h4">
        {winner.display_name === "Me"
          ? "You are the winner "
          : `${winner.display_name} is the winner `}
        with {winner.points} points!
      </Typography>
    </Card>
  ) : null;
};

export default withStyles(styles)(WinnerDisplay);
