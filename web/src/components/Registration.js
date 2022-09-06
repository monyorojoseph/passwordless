import React, { useState } from 'react';
import { Col, Form, Button } from 'react-bootstrap';
import { startRegistration } from '@simplewebauthn/browser';
import axios from 'axios';

const Registration = () => {
    const [ data, setData ] = useState({
        username: '',
        email: ''
    })

    const changeHandler = (e)=> {
        e.persist();
        setData({
            ...data,
            [e.target.name]: e.target.value
        })
    }

    const submitHandler = async(e)=>{
        e.preventDefault();
        console.log(data)
        const config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }

       
        const { data } = await axios.post('/user/registration', data, config);

        try{
            let attResp = await startRegistration(getData())
            console.log(attResp)
        } catch(error){            
            // Some basic error handling
            if (error.name === 'InvalidStateError') {
                console.log('Error: Authenticator was probably already registered by user');
            } else {
                console.log(error);
            }

            throw error;            
        }

    }
    return (
        <Col md={6}>
            <Form onSubmit={submitHandler}>
                <Form.Group className="mb-3" controlId="formBasicEmail">
                    <Form.Label>Username</Form.Label>
                    <Form.Control type="text" placeholder="Enter username" name='username' value={data.username} onChange={changeHandler}/>
                </Form.Group>

                <Form.Group className="mb-3" controlId="formBasicEmail">
                    <Form.Label>Email address</Form.Label>
                    <Form.Control type="email" placeholder="Enter email" name='email' value={data.email} onChange={changeHandler}/>
                </Form.Group>

                <div>
                    <Button type='submit'>
                        Register
                    </Button>
                </div>
            </Form>            
        </Col>
    );
};

export default Registration;