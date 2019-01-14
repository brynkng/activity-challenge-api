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
            competitions={props.competitions}
            showSuccess={props.showSuccess}
            refreshCompetitions={props.refreshCompetitions}
          />
        )}
      />

      <Route
        path="/competition/:id"
        exact
        render={() => (
          <CompetitionDetail
            competitions={props.competitions}
            handleInvite={props.handleInvite}
          />
        )}
      />
    </>
  );
};

export default CompetitionsContainer;
