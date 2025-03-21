import React from "react";
import axios from "axios";
import { Navigate } from "react-router-dom";
import './start.css';

class Start extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            is_loaded: false,
            redirect: false,
            not_started: false,
            finished: false,
        };

        this.handleSubmit = this.handleSubmit.bind(this);
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

    handleSubmit(e) {
        e.preventDefault()
        const token = localStorage.getItem('token');

        const queryParameters = new URLSearchParams(window.location.search)
        const room_id = queryParameters.get("room_id")
        let url = process.env.REACT_APP_BACK_URL + 'exam_sessions/start/' + room_id;
        axios.post(
            url, {
            }, {
                headers: {
                    Authorization: 'Bearer ' + token
                }
            }
        ).then(_ => {
            this.setState({
                redirect: true,
                room_id: room_id,
            })
        }).catch(function (error) {
            let data = error.response.data
            alert(data.detail)
        })
    }

    render() {
        if (this.state.redirect) {
            return <Navigate to={'/exam_sessions/question?room_id=' + this.state.room_id} />
        }
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
                        <h1 className='room-main-label'>Начать экзамен?</h1>
                    </div>
                    <div className='wide-element'>
                        <form onSubmit={this.handleSubmit}>
                            <button className='login-button'>Начать!</button>
                        </form>
                    </div>
                </div>
            </>
        );
    }
}

export default Start;
