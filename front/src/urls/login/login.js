import React from "react";
import './login.css';

class Login extends React.Component {
    render() {
        return (
            <div className='main-centered'>
                <h1 className='login-label'>Вход</h1>
                <input type='text' placeholder='Логин' />
                <input type='password' placeholder='Пароль' />
                <form action="http://localhost:3000/question">
                    <button className='login-button'>Войти</button>
                </form>
            </div>
        );
    }
}

export default Login;
