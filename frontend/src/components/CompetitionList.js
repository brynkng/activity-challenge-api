import React from "react";
import { withStyles } from "@material-ui/core";
import CompetitionSimple from "./CompetitionSimple";
import Typography from "@material-ui/core/es/Typography/Typography";

const styles = theme => ({});

const CompetitionList = props => {
  return props.competitions.length > 0 ? (
    props.competitions.map(c => (
      <CompetitionSimple key={c.id} competition={c} />
    ))
  ) : (
    <Typography variant="title" color="inherit">
      No competitions found
    </Typography>
  );
};

export default withStyles(styles)(CompetitionList);
