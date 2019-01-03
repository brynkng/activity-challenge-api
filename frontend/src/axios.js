import axios from 'axios';
import cookies from 'cookies-js';

const instance = axios.create();

instance.defaults.headers.common['Content-Type'] = 'application/json';

setCsrfHeader();

export function setCsrfHeader() {
    instance.defaults.headers.common["X-CSRFToken"] = cookies.get('csrftoken');
}

export default instance;