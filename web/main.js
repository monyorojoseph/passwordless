import { startRegistration,  browserSupportsWebAuthn } from '@simplewebauthn/browser';
import axios from 'axios';

let DOMAIN = 'https://passwordless-authentincation.herokuapp.com'

// get element ids
const button = document.getElementById('button')
const feedback = document.getElementById('feedback')
const form = document.getElementById('form')

button.addEventListener('click', async()=> {
  button.disabled = true;
  feedback.innerHTML = '';
  let succes = document.createElement("p");
  succes.style.color = 'green';
  let error = document.createElement("p");
  error.style.color = 'red';
  
  const form_data = new FormData(form);
  const data = {email: form_data.get('email'), username:form_data.get('username')};
  if (browserSupportsWebAuthn){
    const config = {
      headers:{
        'Content-Type': 'application/json',
      }}

    try{    
      const { data } = await axios.post(`${DOMAIN}/user/registration`, data, config);
      try{
        // succes.innerText = 'Account Created, now finish verification.';
        const attResp = await startRegistration(data);
        succes.innerText = JSON.stringify(attResp);
        feedback.append(succes);      
        try{
            // POST the response to the endpoint that calls
            // @simplewebauthn/server -> verifyRegistrationResponse()
            const { data:ver_data } = await axios.post(`${DOMAIN}/user/verify-registration`, attResp, config);
            
            // Show UI appropriate for the `verified` status
            if (ver_data && ver_data.verified) {
              succes.innerText = JSON.stringify(ver_data);
              feedback.append(succes)
            } else {
              error.innerText = `Oh no, something went wrong! Response: <pre>${JSON.stringify(
                ver_data,
              )}</pre>`;
              feedback.append(error)
            }
        } catch(error){
          error.innerText = error;
          feedback.append(error); 
        }
      } catch(error){
            // Some basic error handling
            console.log(error)
            if (error.name === 'InvalidStateError') {
              error.innerText = 'Error: Authenticator was probably already registered by user';
              feedback.append(error);      
            } else {
              error.innerText = error;
              feedback.append(error);      
            }
            throw error;
      }
    } catch(error){
      error.innerText = error;
      feedback.append(error);
    }
    
  } else {
    console.log("Nope")
    error.innerText = "Browser doesn't support web authentication"
    feedback.append(error);      
    return;
  }
});
