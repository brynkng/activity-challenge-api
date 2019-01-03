import React from "react";
import {withStyles} from '@material-ui/core/styles';
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Link from "react-router-dom/Link";
import Typography from "@material-ui/core/Typography";
import {logOut} from "../services/auth_api";
import {withRouter} from "react-router";

const styles = theme => ({
});

class Dashboard extends React.Component {

    handleLogout = (e) => {
        e.preventDefault();

        logOut().then(
            r => {
                this.props.handleLogout()
            }
        );
    };

    render() {
        return (
            <>
                Dashboard

                <Link to='/' onClick={this.handleLogout.bind(this)}>Logout</Link>
            </>
        );
    }
}

export default withStyles(styles)(Dashboard);