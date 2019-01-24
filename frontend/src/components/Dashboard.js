import React from "react";
import { withStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import CompetitionsContainer from "./CompetitionsContainer";
import { Route, withRouter, Switch } from "react-router";

const styles = theme => ({});

class Dashboard extends React.Component {
  handleFitbitAuth = () => {
    window.location = this.props.match.params.url;
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
