import React from "react";
import {withStyles} from '@material-ui/core/styles';
import Link from "react-router-dom/Link";
import Typography from "@material-ui/core/Typography";
import {getFitbitData, logOut} from "../services/auth_api";
import Button from "@material-ui/core/Button";
import CircularProgress from '@material-ui/core/CircularProgress';
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
                    this.setState({fitbit_data: r.data.data});
                    console.log(this.state.fitbit_data)
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
                        this.state.fitbit_data.competitions.length > 0 ?
                            this.state.fitbit_data.competitions.map(c => {
                                return (<div>
                                    <h2>{c.name}</h2>
                                    Total Points: {c.points}<br/>
                                    Active Minutes: {c.active_minutes}<br/>
                                    Cardio Zone Minutes: {c.cardio_zone_minutes}<br/>
                                    Peak Zone Minutes: {c.peak_zone_minutes}<br/>
                                </div>);
                            }) :
                            <div>No competitions found</div>
                        :
                        this.state.fitbit_auth_url ?
                            <Button variant="contained" color="primary" onClick={this.handleFitbitAuth}>Authorize
                                Fitbit</Button> :
                            <CircularProgress/>
                }

                <div><Link to='/' onClick={this.handleLogout.bind(this)}>Logout</Link></div>
            </>
        );
    }
}

export default withStyles(styles)(Dashboard);