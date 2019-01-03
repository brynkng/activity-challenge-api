import React from "react";
import {withStyles} from '@material-ui/core/styles';
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import axios from '../axios';
import Typography from "@material-ui/core/Typography";

const styles = theme => ({
    container: {},
    textField: {
        marginLeft: theme.spacing.unit,
        marginRight: theme.spacing.unit,
        width: 200,
    },
    button: {
        margin: '1em .5em'
    }
});

class Register extends React.Component {

    handleSubmit = event => {
        event.preventDefault();

        if (event.target.password.value !== event.target.password_confirmation.value) {
            this.props.showError("Passwords must match!");
        }

        let form_values = Object.values(event.target).reduce((obj, field) => {
            obj[field.name] = field.value;
            return obj
        }, {});

        axios.post('api/register/', form_values)
            .then(r => {
                console.log(r)
                //    do login
            })
            .catch(r => {
                let errors = [].concat(...(Object.values(r.response.data))).join(', ');
                this.props.showError(errors);
            });
    };

    render() {

        const {classes} = this.props;

        return (
            <div className="register">
                <Typography variant="headline" color="inherit">REGISTER</Typography>

                <form className={classes.container} onSubmit={this.handleSubmit}>
                    <TextField
                        id="first_name"
                        label="First Name"
                        className={classes.textField}
                        margin="normal"
                        type="text"
                        name="first_name"
                    />
                    <TextField
                        id="last_name"
                        label="Last Name"
                        className={classes.textField}
                        margin="normal"
                        type="text"
                        name="last_name"
                    /><br/>
                    <TextField
                        id="username"
                        label="Username"
                        className={classes.textField}
                        margin="normal"
                        type="text"
                        name="username"
                        required
                    />
                    <TextField
                        id="email"
                        label="Email"
                        className={classes.textField}
                        margin="normal"
                        type="email"
                        autoComplete="email"
                        name="email"
                        required
                    /><br/>
                    <TextField
                        id="password"
                        label="Password"
                        className={classes.textField}
                        margin="normal"
                        type="password"
                        autoComplete="password"
                        name="password"
                        required
                    />
                    <TextField
                        id="password_confirmation"
                        label="Confirm Password"
                        className={classes.textField}
                        margin="normal"
                        type="password"
                        autoComplete="password"
                        name="password_confirmation"
                        required
                    /><br/>

                    <Button variant="contained" color="primary" type='submit' className={classes.button}>REGISTER</Button>
                </form>
            </div>
        )
    }

}

export default withStyles(styles)(Register);