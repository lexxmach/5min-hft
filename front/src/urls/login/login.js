import React from "react";
import axios from "axios";
import { Navigate } from "react-router-dom";
import './login.css';

class Login extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            login: '',
            password: '',
            redirect: false,
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({
            login: event.target.form[0].value,
            password: event.target.form[1].value,
        });
    }

    handleSubmit(e) {
        e.preventDefault()

        let url = process.env.REACT_APP_BACK_URL + 'login';
        axios.post(
            url, {
                'login': this.state.login,
                'password': this.state.password,
            }
        ).then(res => {
            localStorage.setItem('token', res.data['access_token']);
            this.setState({redirect: true})
        }).catch(function (error) {
            console.log(error.response.data['detail'])
        })
    }

    render() {
        if (this.state.redirect) {
            return <Navigate to={'/question'} />
        }

        return (
            <div className='main-centered'>
                <h1 className='login-label'>Вход</h1>
                <form onSubmit={this.handleSubmit} onChange={this.handleChange}>
                    <input type='text' placeholder='Логин' />
                    <input type='password' placeholder='Пароль' />
                    <button className='login-button'>Войти</button>
                </form>
            </div>
        );
    }
}

export default Login;
