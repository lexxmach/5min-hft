import React from "react";
import axios from "axios";
import './results.css';

class Results extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        };
    }

    componentDidMount() {
        const token = localStorage.getItem('token');

        let url = process.env.REACT_APP_BACK_URL + 'info/';
        axios.get(url, {
            headers: {
                Authorization: 'Bearer ' + token
            }
        }).then(res => {
            let data = res.data;
            this.setState({
                name: data['name'],
                surname: data['surname'],
            })
        });
    }

    render() {
        return (
            <>
                <div className='header'>
                    <a href='/' className='header-href'>Меню</a>
                    <a href='/question' className='header-href'>Вопросы</a>
                    <a href='/leaderboard' className='header-href'>Лидерборд</a>
                    <a href='/create/question' className='header-href'>Создать</a>
                    <a href='/rooms' className='header-href'>Комнаты</a>
                    <a href='/profile' className='header-href'>{this.state.name}</a>
                </div>
                <div className='room-main'>
                    <div className='wide-element-centered'>
                        <h1 className='room-main-label'>Экзамен завершён!</h1>
                    </div>
                </div>
            </>
        );
    }
}

export default Results;
