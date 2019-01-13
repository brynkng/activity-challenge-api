import React from "react";
import { withStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Link from "react-router-dom/Link";
import Typography from "@material-ui/core/Typography";
import { login } from "../services/auth_api";
import { withRouter } from "react-router";

const styles = theme => ({
  container: {
    display: "flex",
    flexWrap: "wrap",
    alignItems: "center"
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200
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
      <div className="login">
        <Typography variant="headline" color="inherit">
          LOGIN
        </Typography>

        <form className={classes.container} onSubmit={this.handleSubmit}>
          <TextField
            id="username"
            label="Username"
            className={classes.textField}
            margin="normal"
            type="text"
            name="username"
          />
          <TextField
            id="password"
            label="Password"
            className={classes.textField}
            margin="normal"
            type="password"
            name="password"
          />

          <Button variant="contained" color="primary" type="submit">
            LOGIN
          </Button>
        </form>

        <Link to="/register">Not registered? Click here</Link>
      </div>
    );
  }
}

export default withRouter(withStyles(styles)(Login));
