import React from 'react';
import { GoogleLogout } from 'react-google-login';

const clientId = '709397836720-avf33rjimjkmjarqe3p00u9megmcpclh.apps.googleusercontent.com';

function Logout() {
    const onSuccess = () => {
        alert('Logout made successfully');
    };

    return (
        <div>
            <GoogleLogout
            clientId={clientId}
            buttontText="Logout"
            onLogoutSuccess={onSuccess}
            style={{marginBottom: '200px'}}
            ></GoogleLogout>
        </div>
    );
}

export default Logout;