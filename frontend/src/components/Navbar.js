import React from "react";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Link from "react-router-dom/Link";
import { withStyles } from "@material-ui/core/styles";
import classNames from "classnames";

const styles = theme => ({
  titleLink: {
    color: "inherit",
    textDecoration: "none",
    "&:hover": { color: "inherit" }
  },
  logout: {
    position: "absolute",
    right: "1em"
  }
});

const NavBar = props => {
  const { classes } = props;

  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="title" color="inherit">
            <Link to="/" className={classes.titleLink}>
              Activity Challenge
            </Link>
          </Typography>
          {props.loggedIn ? (
            <Link
              to="/"
              className={classNames(classes.logout, classes.titleLink)}
              onClick={props.handleLogout.bind(this)}
            >
              Logout
            </Link>
          ) : null}
        </Toolbar>
      </AppBar>
    </div>
  );
};

export default withStyles(styles)(NavBar);
