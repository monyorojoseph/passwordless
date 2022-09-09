import { startRegistration,  browserSupportsWebAuthn } from '@simplewebauthn/browser';
import axios from 'axios';

let DOMAIN = 'https://passwordless-authentincation.herokuapp.com'

// get element ids
const button = document.getElementById('button')
const succes = document.getElementById('succes')
const error = document.getElementById('error')
const form = document.getElementById('form')

button.addEventListener('click', async()=> {
  error.innerText =  '';
  succes.innerText = '';

  const form_data = new FormData(form);
  const data = {email: form_data.get('email'), username:form_data.get('username')};
  if (browserSupportsWebAuthn){
    console.log("hey Vite js")
    console.log(`${import.meta.env.MODE}`)
    const config = {
      headers:{
        'Content-Type': 'application/json',
      }}

    let attResp;

    axios.post(`${DOMAIN}/user/registration`, data, config)
    .then(res=>res.data)
    .then(async(data)=> {
      try{
        console.log('We made')
        attResp = await startRegistration(data);
        console.log('It')
        console.log(attResp)
      } catch(error){
            // Some basic error handling
            console.log(error)
            if (error.name === 'InvalidStateError') {
              error.innerText = 'Error: Authenticator was probably already registered by user';
            } else {
              error.innerText = error;
            }
      
            throw error;
      }
    })
    .catch(error => {
      console.log(error)
    })
        
    // POST the response to the endpoint that calls
    // @simplewebauthn/server -> verifyRegistrationResponse()
    axios.post(`${DOMAIN}/user/verify-registration`, JSON.stringify(attResp), config).
    then(res => res.data)
    .then(async(data)=> {
      console.log(data)
      // Show UI appropriate for the `verified` status
      if (data && data.verified) {
        elemSuccess.innerHTML = 'Success!';
      } else {
        elemError.innerHTML = `Oh no, something went wrong! Response: <pre>${JSON.stringify(
          data,
        )}</pre>`;
      }

    })
    .catch(error => {
      console.log(error)
    });

  } else {
    console.log("Nope")
    error.innerText = "Browser doesn't support web authentication"
    return;
  }
});
