import React from "react";
import ReactDOM from "react-dom";
import {Route, Switch, BrowserRouter} from "react-router-dom";
import Home from "./Home";
import {CookiesProvider} from 'react-cookie';


const App = () => (

    <BrowserRouter>
        <CookiesProvider>
            <main>
                {/*<DataProvider endpoint="api/competitions/" render={data => <Table data={data}/>}/>*/}
                <Switch>
                    {/*<Route path="/authenticate" component={Auth}/>*/}
                    <Route path="/" component={Home}/>
                </Switch>
            </main>
        </CookiesProvider>
    </BrowserRouter>
);

const wrapper = document.getElementById("app");

wrapper ? ReactDOM.render(<App/>, wrapper) : null;