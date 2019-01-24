import React from "react";
import { Route } from "react-router-dom";
import CompetitionList from "./CompetitionList";
import CompetitionDetail from "./CompetitionDetail";

const CompetitionsContainer = props => {
  return (
    <>
      <Route
        path="/"
        exact
        render={() => (
          <CompetitionList
            showSuccess={props.showSuccess}
            showError={props.showError}
          />
        )}
      />

      <Route
        path="/competition/:id"
        exact
        render={() => (
          <CompetitionDetail
            handleInvite={props.handleInvite}
            showError={props.showError}
            showSuccess={props.showSuccess}
          />
        )}
      />
    </>
  );
};

export default CompetitionsContainer;
