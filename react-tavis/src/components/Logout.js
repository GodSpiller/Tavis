import React from 'react';
import { GoogleLogout } from 'react-google-login';

const clientId = '709397836720-avf33rjimjkmjarqe3p00u9megmcpclh.apps.googleusercontent.com';

function Logout() {
    const onSuccess = () => {
        alert('Logout made successfully');
    };

    return (
        <div style={{
            position: 'absolute', left: '56%', top: '61%',
            transform: 'translate(-50%, -50%)'
        }}>
            <GoogleLogout
            clientId={clientId}
            buttontText="Logout"
            onLogoutSuccess={onSuccess}
            style={{marginBottom: '200px'}}
            >Logout</GoogleLogout>
        </div>
    );
}

export default Logout;