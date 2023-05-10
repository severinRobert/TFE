import axios from 'axios'

export const headers = () => { 
  console.log('headers')
  console.log(localStorage.getItem('token'))
  return axios.create({
    baseURL: `http://${import.meta.env.VITE_API_URL}`,
    timeout: 5000,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    }
  });
}

export const athentificationHeaders = () => { 
  console.log('headers')
  console.log(localStorage.getItem('token'))
  return axios.create({
    baseURL: `http://${import.meta.env.VITE_API_URL}`,
    timeout: 5000,
    headers: {
      'accept': 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Access-Control-Allow-Origin': '*'
    }
  });
}
