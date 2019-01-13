import { Route } from "react-router-dom";
import React from "react";
import Login from "./Login";
import Register from "./Register";

const Auth = outer_props => (
  <>
    <Route path="/" exact render={props => <Login {...outer_props} />} />

    <Route
      path="/register"
      exact
      render={props => <Register {...outer_props} />}
    />
  </>
);

export default Auth;
