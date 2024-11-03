import React from "react";
import logo from '../../resources/logo.png'
import './main.css';

class Main extends React.Component {
    render() {
        return (
            <div className='main'>
                <img src={logo} alt='logo' className='logo' />
                <div className='line'>
                    <h1>Добро пожаловать в </h1>
                    <h1 className='name'>HFT in 5 minutes</h1>
                </div>
                <span>Погрузитесь в мир IT вместе с нами! Для начала работы войдите или зарегистрируйтесь по кнопкам ниже.</span>
                <form action="http://localhost:3000/login">
                    <button className='green-button'>Войти</button>
                </form>
                <button className='blue-button'>Зарегистрироваться</button>
            </div>
        );
    }
}

export default Main;
