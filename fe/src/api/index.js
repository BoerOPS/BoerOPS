import axios from 'axios'

var instance = axios.create();

instance.interceptors.request.use(
  (config) => {
    if (config.url !== '/login') {
      config.headers.TOKEN = localStorage.getItem('access_token');
    }
    config.baseURL = '';
    config.timeout = 50 * 1000;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

instance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default instance;
