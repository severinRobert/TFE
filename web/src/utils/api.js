import axios from 'axios'

export const headers = () => {
  let api = axios.create({
    baseURL: `${import.meta.env.VITE_API_URL}`,
    timeout: 5000,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    }
  });
  api.interceptors.response.use((response) => response, (error) => {
    if([401, 403].includes(error.response.status) && localStorage.getItem('user') && localStorage.getItem('password')) {
      authenticationHeaders().post("/users/login", {
        username: localStorage.getItem('user'),
        password: localStorage.getItem('password'),
      }).then((response) => {
        console.log("TOKEN REFRESHED", response.data.access_token);
        localStorage.setItem('token', response.data.access_token);
      }).catch((error) => {
        console.log("headers error 403", error.response);
      });
    }
    return Promise.reject(error);
  });
  return api;
}

export const authenticationHeaders = () => {
  let api = axios.create({
    baseURL: `${import.meta.env.VITE_API_URL}`,
    timeout: 5000,
    headers: {
      'accept': 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Access-Control-Allow-Origin': '*'
    }
  });
  api.interceptors.response.use((response) => response, (error) => {
    return Promise.reject(error);
  });
  return api;
}
