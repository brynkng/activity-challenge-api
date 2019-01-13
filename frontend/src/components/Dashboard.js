import React from "react";
import { withStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import { getFitbitData } from "../services/data_provider";
import Button from "@material-ui/core/Button";
import CircularProgress from "@material-ui/core/CircularProgress";
import CompetitionList from "./CompetitionList";
import { Route, Switch } from "react-router-dom";
import CompetitionDetail from "./CompetitionDetail";

const styles = theme => ({});

class Dashboard extends React.Component {
  state = {
    fitbit_auth_url: null,
    competitions: null,
    show_competition: null
  };

  handleFitbitAuth = () => {
    window.location = this.state.fitbit_auth_url;
  };

  componentDidMount() {
    getFitbitData()
      .then(r => {
        if (r.data.authorized) {
          console.log(r.data.data)
          this.setState({ competitions: r.data.data.competitions });
        } else if (r.data.auth_url) {
          if(r.data.errors) {
            this.props.showError(r.data.errors);
            console.log(r.data.errors)
          }
          this.setState({ fitbit_auth_url: r.data.auth_url });
        }
      })
      .catch(r => {
        this.props.showError("Server error. Please contact developer.");
        console.log(r.data);

        if (r.response.data.auth_url) {
          this.setState({ fitbit_auth_url: r.response.data.auth_url });
        }
      });
  }

  render() {
    return (
      <>
        {this.state.competitions ? (
          <Switch>
            <Route
              path="/"
              exact
              render={props => (
                <CompetitionList
                  {...props}
                  competitions={this.state.competitions}
                />
              )}
            />

            <Route
              path="/competition/:id"
              exact
              render={props => (
                <CompetitionDetail
                  {...props}
                  competitions={this.state.competitions}
                />
              )}
            />
          </Switch>
        ) : this.state.fitbit_auth_url ? (
          <Button
            variant="contained"
            color="primary"
            onClick={this.handleFitbitAuth}
          >
            Authorize Fitbit
          </Button>
        ) : (
          <CircularProgress />
        )}
      </>
    );
  }
}

export default withStyles(styles)(Dashboard);
