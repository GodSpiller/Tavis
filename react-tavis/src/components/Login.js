import React from 'react';
import { GoogleLogin } from 'react-google-login';

const clientId = '709397836720-avf33rjimjkmjarqe3p00u9megmcpclh.apps.googleusercontent.com';

function Login() {
    const onSuccess = (res) => {
        console.log('[Login Success] currentUser:', res.profileObj);

    };

    const onFailure = (res) => {
        console.log('[Login failed] res:', res)
    };

    return (
        <div>
            <GoogleLogin 
            clientId={clientId}
            buttonText="Login"
            onSuccess={onSuccess}
            onFailure={onFailure}
            cookiePolicy={'single_host_origin'}
            isSignedIn={true}
            />
        </div>
    );

}

export default Login;