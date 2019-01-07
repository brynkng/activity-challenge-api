import React from "react";
import {withStyles} from '@material-ui/core/styles';
import Link from "react-router-dom/Link";
import Typography from "@material-ui/core/Typography";
import {getFitbitData, logOut} from "../services/auth_api";
import Button from "@material-ui/core/Button";
import {obj_arr_to_str} from "../services/helpers";

const styles = theme => ({});

class Dashboard extends React.Component {

    state = {
        fitbit_auth_url: null,
        fitbit_data: null,
    };

    handleLogout = (e) => {
        e.preventDefault();

        logOut().then(
            r => {
                this.props.handleLogout()
            }
        );
    };

    handleFitbitAuth = () => {
        window.location = this.state.fitbit_auth_url;
    };

    componentDidMount() {
        getFitbitData()
            .then(r => {
                if (r.data.authorized) {
                    let data = r.data.data,
                        active_minutes = data.summary.fairlyActiveMinutes + data.summary.veryActiveMinutes,
                        steps = data.summary.steps;

                    this.setState({fitbit_data: {active_minutes: active_minutes, steps: steps}});
                } else if (r.data.auth_url) {
                    this.setState({fitbit_auth_url: r.data.auth_url});
                }
            })
            .catch(r => {
                this.props.showError(obj_arr_to_str(r.response.data.errors));
                if (r.response.data.auth_url) {
                    this.setState({fitbit_auth_url: r.response.data.auth_url});
                }
            })
    }

    render() {
        return (
            <>
                <Typography variant="headline" color="inherit">DASHBOARD</Typography>

                {
                    this.state.fitbit_data ?
                        <div>Active Minutes: {this.state.fitbit_data.active_minutes}<br/>Steps: {this.state.fitbit_data.steps}</div> :
                    this.state.fitbit_auth_url ?
                        <Button variant="contained" color="primary" onClick={this.handleFitbitAuth}>Authorize Fitbit</Button> :
                        <div>Loading...</div>
                }

                <div><Link to='/' onClick={this.handleLogout.bind(this)}>Logout</Link></div>
            </>
        );
    }
}

export default withStyles(styles)(Dashboard);