import React from "react";
import axios from "axios";
import { Navigate } from "react-router-dom";
import './register.css';

class Register extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: '',
            surname: '',
            login: '',
            password: '',
            redirect: false,
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({
            name: event.target.form[0].value,
            surname: event.target.form[1].value,
            login: event.target.form[2].value,
            password: event.target.form[3].value,
        });
    }

    handleSubmit(e) {
        e.preventDefault()

        let url = process.env.REACT_APP_BACK_URL + 'register';
        axios.post(url, {
            'user_credentials': {
                'login': this.state.login,
                'password': this.state.password,
            },
            'user_info': {
                'name': this.state.name,
                'surname': this.state.surname,
            }
        }).then(res => {
            this.setState({redirect: true})
        }).catch(function (error) {
            console.log(error.response.data['detail'])
        })
    }

    render() {
        if (this.state.redirect) {
            return <Navigate to={'/login'} />
        }
        return (
            <div className='main-centered'>
                <h1 className='register-label'>Регистрация</h1>
                <form onSubmit={this.handleSubmit} onChange={this.handleChange}>
                    <input name='name' type='text' placeholder='Имя' />
                    <input name='surname' type='text' placeholder='Фамилия' />
                    <input name='login' type='text' placeholder='Логин' />
                    <input name='password' type='password' placeholder='Пароль' />
                    <button className='register-button'>Зарегистрироваться</button>
                </form>
            </div>
        );
    }
}

export default Register;
