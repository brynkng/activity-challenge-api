import {Route} from "react-router-dom";
import React from "react";
import Login from "./Login";
import Register from "./Register";

const Auth = (outer_props) => (
    <>
        <Route
            path="/"
            exact
            render={(props) => <Login {...props} showError={outer_props.showError} />}
        />

        <Route
            path="/register"
            exact
            render={(props) => <Register {...props} showError={outer_props.showError} />}
        />
    </>
);

export default Auth;