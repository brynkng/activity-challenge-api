import React from "react";
import Card from "@material-ui/core/Card";
import Table from "@material-ui/core/Table";
import TableRow from "@material-ui/core/es/TableRow/TableRow";
import TableCell from "@material-ui/core/es/TableCell/TableCell";
import { withStyles } from "@material-ui/core";
import Typography from "@material-ui/core/Typography";
import TableBody from "@material-ui/core/TableBody";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import ExpandLessIcon from "@material-ui/icons/ExpandLess";

const styles = theme => ({
  title: {
    margin: ".5em 0"
  },
  card: {
    paddingTop: "1.5em",
    marginBottom: "1em",
    cursor: "pointer"
  },
  table: {
    marginTop: "1em"
  },
  point_factor: {
    display: "inline-block",
    marginLeft: "0.2em"
  }
});

class PointDisplay extends React.Component {
  state = {
    expanded: false
  };

  handleClick = () => {
    let expanded = this.state.expanded;
    this.setState({ expanded: !expanded });
  };

  render() {
    const { classes } = this.props;

    return (
      <Card className={classes.card} onClick={this.handleClick}>
        <Typography variant="h6">{this.props.name}</Typography>

        <Typography variant="inherit">
          <Table className={this.props.classes.table}>
            <TableBody>
              <TableRow>
                <TableCell>Total Points</TableCell>
                <TableCell align="right">
                  <Typography variant="display1">
                    {this.props.point_details.points}
                  </Typography>
                </TableCell>
              </TableRow>
              {this.state.expanded ? (
                <>
                  <TableRow>
                    <TableCell>Active Minutes</TableCell>
                    <TableCell>
                      {this.props.point_details.active_minutes}
                      <Typography
                        variant="caption"
                        className={classes.point_factor}
                      >
                        (x{this.props.point_details.active_minute_factor})
                      </Typography>
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Cardio Zone Minutes</TableCell>
                    <TableCell>
                      {this.props.point_details.cardio_zone_minutes}
                      <Typography
                        variant="caption"
                        className={classes.point_factor}
                      >
                        (x{this.props.point_details.cardio_zone_factor})
                      </Typography>
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Peak Zone Minutes</TableCell>
                    <TableCell>
                      {this.props.point_details.peak_zone_minutes}
                      <Typography
                        variant="caption"
                        className={classes.point_factor}
                      >
                        (x{this.props.point_details.peak_zone_factor})
                      </Typography>
                    </TableCell>
                  </TableRow>
                </>
              ) : null}
            </TableBody>
          </Table>
        </Typography>

        {this.state.expanded ? (
          <ExpandLessIcon fontSize="large" />
        ) : (
          <ExpandMoreIcon fontSize="large" />
        )}
      </Card>
    );
  }
}

export default withStyles(styles)(PointDisplay);
