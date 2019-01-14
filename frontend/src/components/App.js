import React from "react";
import ReactDOM from "react-dom";
import { Route, Switch, BrowserRouter, HashRouter } from "react-router-dom";
import Layout from "./Layout";
import { CookiesProvider } from "react-cookie";
import CssBaseline from "@material-ui/core/es/CssBaseline/CssBaseline";

const App = () => (
  <HashRouter>
    <CookiesProvider>
      <CssBaseline>
        <main>
          {/*<DataProvider endpoint="api/competitions/" render={data => <Table data={data}/>}/>*/}
          <Switch>
            {/*<Route path="/authenticate" component={Auth}/>*/}
            <Route path="/" component={Layout} />
          </Switch>
        </main>
      </CssBaseline>
    </CookiesProvider>
  </HashRouter>
);

const wrapper = document.getElementById("app");

wrapper ? ReactDOM.render(<App />, wrapper) : null;
