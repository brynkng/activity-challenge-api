import React from "react";
import ReactDOM from "react-dom";
import {Route, Switch, BrowserRouter, HashRouter} from "react-router-dom";
import Layout from "./Layout";
import {CookiesProvider} from 'react-cookie';


const App = () => (

    <HashRouter>
        <CookiesProvider>
            <main>
                {/*<DataProvider endpoint="api/competitions/" render={data => <Table data={data}/>}/>*/}
                <Switch>
                    {/*<Route path="/authenticate" component={Auth}/>*/}
                    <Route path="/" component={Layout}/>
                </Switch>
            </main>
        </CookiesProvider>
    </HashRouter>
);

const wrapper = document.getElementById("app");

wrapper ? ReactDOM.render(<App/>, wrapper) : null;