import axios from 'axios';
import cookies from 'cookies-js';

const instance = axios.create();

setAuthHeader();

export function setAuthHeader() {
    instance.defaults.headers.common['Content-Type'] = 'application/json';
    instance.defaults.headers.common["X-CSRFToken"] = cookies.get('csrftoken');
}

export default instance;