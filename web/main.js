import { startRegistration,  browserSupportsWebAuthn } from '@simplewebauthn/browser';
import axios from 'axios';

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
    const config = {
      headers:{
        'Content-Type': 'application/json',
        // 'Access-Control-Allow-Origin': '*'
      }}

    let attResp;

    axios.post("http://localhost:8000/user/registration", data, config)
    .then(res=>res.data)
    .then(async(data)=> {
      try{
        console.log('We made')
        attResp = await startRegistration(data);
        console.log('It')
      } catch(error){
            // Some basic error handling
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
        
  } else {
    console.log("Nope")
    error.innerText = "Browser doesn't support web authentication"
    return;
  }
});
