import React from "react";
import { withRouter } from "react-router-dom";
import Snackbar from "@material-ui/core/Snackbar";
import { Notifier } from "./Notifier";
import Auth from "./Auth";
import NavBar from "./Navbar";
import withStyles from "@material-ui/core/styles/withStyles";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import { loggedIn, logOut } from "../services/auth_api";
import Dashboard from "./Dashboard";
import * as qs from "query-string";

const styles = theme => ({
  root: {
    flexGrow: 1,
    justifyContent: "center",
    maxWidth: "1024px",
    margin: "0 auto"
  },
  paper: {
    padding: theme.spacing.unit * 2,
    textAlign: "center",
    color: theme.palette.text.secondary
  }
});

class Layout extends React.Component {
  state = {
    loggedIn: false,
    open: false,
    snackbar_variant: "success",
    snackbar_message: ""
  };

  componentDidMount() {
    if (!this.state.loggedIn && loggedIn()) {
      this.setState({ loggedIn: true });
    }

    const params = qs.parse(this.props.location.search);
    if (params.errors) {
      this.showError(params.errors);
    }
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.location.state && nextProps.location.state.error) {
      this.showError(nextProps.location.state.error);
    }
  }

  handleClose = (event, reason) => {
    if (reason === "clickaway") {
      return;
    }

    this.setState({ open: false });
  };

  handleLoggedIn = () => {
    this.props.history.replace("/");
    this.setState({ loggedIn: true });
  };

  handleLogout = e => {
    e.preventDefault();

    logOut()
      .then(r => {
        this.props.history.replace("/");
        this.setState({ loggedIn: false });
      })
      .catch(r => {
        console.log(r);
        this.showError("Error logging out!");
      });
  };

  showError = error => {
    this.setState({
      open: true,
      snackbar_variant: "error",
      snackbar_message: error
    });
  };

  showSuccess = message => {
    this.setState({
      open: true,
      snackbar_variant: "success",
      snackbar_message: message
    });
  };

  render() {
    const { classes } = this.props;

    return (
      <Grid container className={classes.root}>
        <Grid item xs={12}>
          <NavBar
            handleLogout={this.handleLogout}
            loggedIn={this.state.loggedIn}
          />
          <Paper className={classes.paper}>
            {this.state.loggedIn ? (
              <Dashboard
                showError={this.showError}
                showSuccess={this.showSuccess}
              />
            ) : (
              <Auth
                showError={this.showError}
                handleLoggedIn={this.handleLoggedIn}
              />
            )}

            <Snackbar
              anchorOrigin={{
                vertical: "bottom",
                horizontal: "left"
              }}
              open={this.state.open}
              autoHideDuration={6000}
              onClose={this.handleClose}
            >
              <Notifier
                onClose={this.handleClose}
                variant={this.state.snackbar_variant}
                message={this.state.snackbar_message}
              />
            </Snackbar>
          </Paper>
        </Grid>
      </Grid>
    );
  }
}

export default withRouter(withStyles(styles)(Layout));
