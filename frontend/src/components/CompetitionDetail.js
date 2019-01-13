import React from "react";
import { withStyles } from "@material-ui/core";
import Typography from "@material-ui/core/Typography";
import { withRouter } from "react-router";
import CompetitionInviter from "./CompetitionInviter";
import Grid from "@material-ui/core/Grid";
import PointDisplay from "./PointDisplay";


const styles = theme => ({
  title: {
    margin: '.5em 0'
  },
  card: {
    padding: '1.5em 0'
  },
  table: {
    marginTop: '1em'
  }
});

const CompetitionDetail = props => {
  const { classes } = props;
  const id = parseInt(props.match.params.id);
  let competition = props.competitions.filter(c => {
    return id === c.id;
  })[0];

  return (
    <>
      <Typography variant="display1" className={classes.title}> {competition.name}</Typography>

      <Grid container spacing={24} className={classes.container}>
        <Grid item xs={12} md={7}>
          <PointDisplay name={'Me'} point_details={competition.point_details}/>
          {competition.competition_members.map(m => <PointDisplay key={m.profile_id} name={m.display_name} point_details={m}/>)}
        </Grid>
        <Grid item xs={12} md={5}>
          <CompetitionInviter competition={competition} />
        </Grid>
      </Grid>
    </>
  );
};

export default withRouter(withStyles(styles)(CompetitionDetail));
