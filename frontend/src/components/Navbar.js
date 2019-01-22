import React from "react";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Link from "react-router-dom/Link";
import { withStyles } from "@material-ui/core/styles";
import classNames from "classnames";
import LogoutIcon from "@material-ui/icons/ExitToApp";

const styles = theme => ({
  title: { flexGrow: 1 },
  link: {
    color: "inherit",
    textDecoration: "none",
    "&:hover": { color: "inherit" }
  }
});

const NavBar = props => {
  const { classes } = props;

  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="title" color="inherit" className={classes.title}>
            <Link to="/" className={classes.link}>
              Activity Challenge
            </Link>
          </Typography>
          {props.loggedIn ? (
            <Link
              to="/"
              className={classes.link}
              onClick={props.handleLogout.bind(this)}
            >
              <LogoutIcon fontSize="large" />
            </Link>
          ) : null}
        </Toolbar>
      </AppBar>
    </div>
  );
};

export default withStyles(styles)(NavBar);
