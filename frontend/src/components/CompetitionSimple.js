import React from "react";
import { withStyles } from "@material-ui/core";
import Typography from "@material-ui/core/es/Typography/Typography";
import { Link } from "react-router-dom";
import Card from "@material-ui/core/es/Card/Card";
import moment from 'moment';
import WinnerDisplay from "./WinnerDisplay";

const styles = theme => ({
  container: {
    margin: "1em 0",
    padding: "1em",
    cursor: "pointer",
    "&:hover": { background: "#eee" },
    transition: ".3s background"
  },
  titleLink: {
    color: "inherit",
    textDecoration: "none",
    "&:hover": { color: "inherit" }
  }
});

const CompetitionSimple = props => {
  const { classes } = props;

  return (
    <Link
      to={`/competition/${props.competition.id}`}
      className={classes.titleLink}
    >
      <Card className={classes.container}>
        <Typography variant="title">{props.competition.name}</Typography>

        {!props.competition.current ? (
          <>
            <WinnerDisplay winner={props.competition.winner}/>
            <Typography variant="h6">
              Ended {moment(props.competition.end).format("MMMM Do")}
            </Typography>
          </>
        ) : (
          <>
            <Typography variant="display1">
              {props.competition.points}
            </Typography>
            <Typography variant="h6">{moment(props.competition.start).format("MMMM D")} - {moment(props.competition.end).format('D')}</Typography>
          </>
        )}
      </Card>
    </Link>
  );
};

export default withStyles(styles)(CompetitionSimple);
