import React, { useState } from 'react';
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "firebase/auth";

function AuthForm() {
    const auth = getAuth();
    const [errorString, setErrorString] = useState('');
    
    function setError(errorMessage: string) {
        errorMessage = errorMessage.replace('Firebase:', '')
        setErrorString(errorMessage)
    }

    function signup(mail: string, password: string) {
        createUserWithEmailAndPassword(auth, mail, password)
            .then((userCredential) => {
                const user = userCredential.user;
            })
            .catch((error) => {
                setError(error.message)
        });
    }

    function login(mail: string, password: string) {
        signInWithEmailAndPassword(auth, mail, password)
            .then((userCredential) => {
                const user = userCredential.user;
            })
            .catch((error) => {
                setError(error.message)
            });
    }
    
    function submitForm(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        const mail = formData.get('email') as string;
        const password = formData.get('password') as string;

        const action = (event.nativeEvent as any).submitter.name;

        if (action === 'signup') {
            signup(mail, password)
        } else if (action === 'login') {
            login(mail, password)
        }
    }

    return (
        <div className='w-96'>
            <div className="card w-96 bg-base-100 card-sm shadow-sm bg-base-200">
                <div className="card-body">
                    <h2 className='card-title'>Sign Up</h2>
                    <form onSubmit={submitForm}>
                        <div>
                            <input type="email" id="email" name="email" className="input" placeholder='Email' required />
                        </div>
                        <div className='mt-2'>
                            <input type="password" id="password" name="password" className="input" placeholder='Password'  required />
                        </div>
                        <div className='mt-2 join'>
                            <button type="submit" name='signup' className='btn btn-soft btn-primary join-item'>Sign Up</button>
                            <button type="submit" name='login' className='btn btn-soft btn-secondary join-item'>Log In</button>
                        </div>
                    </form>
                </div>
            </div>
            {errorString !== '' ?
                <div role="alert" className="alert alert-error alert-soft mt-4">
                    <span>Something went wrong; {errorString}</span>
                </div>
                : <div></div>
            }
        </div>
    );
};

export default AuthForm;