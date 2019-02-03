import React from "react";
import { withStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import CompetitionsContainer from "./CompetitionsContainer";
import { Route, withRouter, Switch } from "react-router";

const styles = theme => ({});

class Dashboard extends React.Component {
  handleFitbitAuth = () => {
    let state = this.props.history.location.state;
    if (state && state.auth_url) {
      window.location = state.auth_url;
    } else {
      this.props.showError("Error accessing auth url");
    }
  };

  render() {
    return (
      <>
        <Switch>
          <Route path="/fitbit_auth/">
            <Button
              variant="contained"
              color="primary"
              onClick={this.handleFitbitAuth}
            >
              Authorize Fitbit
            </Button>
          </Route>

          <Route
            path="/"
            render={() => (
              <CompetitionsContainer
                showSuccess={this.props.showSuccess}
                showError={this.props.showError}
              />
            )}
          />
        </Switch>
      </>
    );
  }
}

export default withStyles(styles)(withRouter(Dashboard));
