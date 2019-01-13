import React from "react";
import { withStyles } from "@material-ui/core";
import Typography from "@material-ui/core/es/Typography/Typography";
import { Link } from "react-router-dom";

const styles = theme => ({
  container: {
    border: "1px solid #eee",
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
      <div className={classes.container}>
        <Typography variant="title">
          {" "}
          {props.competition.name} - {props.competition.points} points
        </Typography>
      </div>
    </Link>
  );
};

export default withStyles(styles)(CompetitionSimple);
