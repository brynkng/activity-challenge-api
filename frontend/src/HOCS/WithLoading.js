import React from "react";
import CircularProgress from "@material-ui/core/CircularProgress";

const WithLoading = props => {
  return props.isLoaded ? <>{props.children}</> : <CircularProgress />;
};

export { WithLoading };
