// HTTP requests for the Flask server

const BASE_URL = 'http://localhost:5000';

export const fetchFromURI = uri => {
  return fetch(uri)
    .then(res => res.json())
    .catch(err => console.log(err));
}

// send a JSON object to the Flask server
// using HTTP POST
 
export const portToFlask = (endpoint, data) => {
  let uri = BASE_URL + endpoint;
  let options = {
    headers: {'Content-Type':'application/json' },
    method: 'POST',
    body: JSON.stringify({ data })
  };
  return fetch(uri,options)
    .then(res => res.json())
    .catch(err => console.log(err))
}

