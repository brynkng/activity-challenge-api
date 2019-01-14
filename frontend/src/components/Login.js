import React from "react";
import { withStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Link from "react-router-dom/Link";
import Typography from "@material-ui/core/Typography";
import { login } from "../services/auth_api";
import { withRouter } from "react-router";
import Grid from "@material-ui/core/Grid";

const styles = theme => ({
  container: {
    margin: "0 auto",
    maxWidth: "40em"
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200
  },
  register: {
    margin: "1em 0",
    display: "block"
  },
  login: {
    margin: "1em 0"
  }
});

class Login extends React.Component {
  handleSubmit = event => {
    event.preventDefault();

    login(event.target.username.value, event.target.password.value)
      .then(r => {
        if (r.data.success) {
          this.props.handleLoggedIn();
        } else {
          this.props.showError(r.data.message);
        }
      })
      .catch(r => {
        this.props.showError(r.response.data.detail);
        console.log(r);
      });
  };

  render() {
    const { classes } = this.props;

    return (
      <>
        <Typography variant="headline" color="inherit">
          LOGIN
        </Typography>

        <form className={classes.container} onSubmit={this.handleSubmit}>
          <Grid container alignItems="center">
            <Grid item xs={12} md={4}>
              <TextField
                id="username"
                label="Username"
                className={classes.textField}
                margin="normal"
                type="text"
                name="username"
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField
                id="password"
                label="Password"
                className={classes.textField}
                margin="normal"
                type="password"
                name="password"
              />
            </Grid>

            <Grid item xs={12} md={4}>
              <Button
                variant="contained"
                color="primary"
                type="submit"
                className={classes.login}
              >
                LOGIN
              </Button>
            </Grid>
          </Grid>
        </form>

        <Link to="/register" className={classes.register}>
          <Typography variant="button">register</Typography>
        </Link>
      </>
    );
  }
}

export default withRouter(withStyles(styles)(Login));
