// HTTP requests for the Flask server

export const fetchFromURI = uri => {
  return fetch(uri)
    .then(res => res.json())
    .catch(err => console.log(err));
}