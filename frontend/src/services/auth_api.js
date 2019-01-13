import axios, { setCsrfHeader } from "../axios";

function login(username, password) {
  return axios
    .post("api/login/", { username: username, password: password })
    .then(r => {
      if (r.data.success) {
        localStorage.setItem("loggedIn", "true");
        setCsrfHeader();
      }

      return r;
    });
}

function loggedIn() {
  return localStorage.getItem("loggedIn") === "true";
}

function logOut() {
  return axios.post("api/logout/").then(r => {
    if (r.data.success) {
      localStorage.setItem("loggedIn", "false");
    }

    return r;
  });
}

function register(form_values) {
  return axios.post("api/register/", form_values);
}

export { login, register, loggedIn, logOut };
