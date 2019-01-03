import React from "react";
import { withStyles } from '@material-ui/core/styles';
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Link from "react-router-dom/es/Link";

const styles = theme => ({
    container: {
        display: 'flex',
        flexWrap: 'wrap',
        alignItems: 'center'
    },
    textField: {
        marginLeft: theme.spacing.unit,
        marginRight: theme.spacing.unit,
        width: 200,
    },
});

class Login extends React.Component {

    handleSubmit = event => {
        console.log(event.target.email.value)
        console.log(event.target.password.value)
        event.preventDefault();
    };

    render() {
        const { classes } = this.props;

        return (
            <div className="login">
                <h2>LOGIN</h2>

                <form className={classes.container} onSubmit={this.handleSubmit}>
                    <TextField
                        id="email"
                        label="Email"
                        className={classes.textField}
                        margin="normal"
                        type="email"
                        autoComplete="email"
                        name="email"
                    />
                    <TextField
                        id="password"
                        label="Password"
                        className={classes.textField}
                        margin="normal"
                        type="password"
                        autoComplete="password"
                        name="password"
                    />

                    <Button variant="contained" color="primary" type='submit'>LOGIN</Button>
                </form>

                <Link to="/register">Not registered? Click here</Link>
            </div>
        );
    }
}

export default withStyles(styles)(Login);
