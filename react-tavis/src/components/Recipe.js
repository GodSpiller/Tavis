import React from 'react';
import Logo from '../images/temp.png'
import './Recipe.css'

function Recipe (props) {
    
    return (
    <div class="container" onClick={() => alert(props.alert)}>
        <img src={Logo} alt="Frozen coffee shake"/>
        <h1>{props.title}</h1>
    </div>
    )
}

export default Recipe;