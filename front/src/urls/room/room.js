import React from "react";
import axios from "axios";
import { exportToExcel  } from "react-json-to-excel";
import './room.css';

class Room extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            is_root: true,
            rooms: [],
            room_name: '',
        };

        this.onResults = this.onResults.bind(this);
        this.genRoomsList = this.genRoomsList.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    componentDidMount() {
        const token = localStorage.getItem('token');

        let url = process.env.REACT_APP_BACK_URL + 'is_root';
        axios.get(url, {
            headers: {
                Authorization: 'Bearer ' + token
            }
        }).then(res => {
            this.setState({is_root: res.data});
        });

        url = process.env.REACT_APP_BACK_URL + 'info/';
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

        url = process.env.REACT_APP_BACK_URL + 'rooms/';
        axios.get(url, {
            headers: {
                Authorization: 'Bearer ' + token
            }
        }).then(res => {
            let data = res.data;
            this.setState({
                rooms: data,
            })
        });
    }

    onResults(i) {
        const token = localStorage.getItem('token');

        let url = process.env.REACT_APP_BACK_URL + 'exam_sessions/results/' + i.toString();
        axios.get(url, {
            headers: {
                Authorization: 'Bearer ' + token
            }
        }).then(res => {
            let data = res.data;
            exportToExcel(data['questions'], 'results_' + i.toString() + '.json')
        }).catch(function (error) {
            let data = error.response.data
            alert(data.detail)
        });
    }

    genRoomsList() {
        let result = []

        for (let i = 0; i < this.state.rooms.length; ++i) {
            result.push(
                <div className='room-list-room'>
                    <div className='splitter'>
                        <div className='room-list-room-number'>
                            <span>{i + 1}.</span>
                            <span className='bold'>{this.state.rooms[i].name}</span>
                        </div>
                        <span>id = {this.state.rooms[i].id}</span>
                    </div>
                    <div className='room-list-room-buttons'>
                        <button className='room-button' onClick={(e) => {e.preventDefault(); window.location.href='/create/question';}}>Добавить вопрос</button>
                        <button className='room-button-blue' onClick={() => {this.onResults(this.state.rooms[i].id)}}>Результаты</button>
                    </div>
                    <a href={process.env.REACT_APP_FRONT_URL + 'exam_sessions/start?room_id=' + this.state.rooms[i].id.toString()} className='room-start-ref'>Ссылка на старт экзамена</a>
                </div>
            )
        }

        return result
    }

    handleChange(event) {
        this.setState({
            room_name: event.target.form[0].value,
            duration: event.target.form[1].value,
            start_time: event.target.form[2].value,
            end_time: event.target.form[3].value
        });
    }

    handleSubmit(e) {
        e.preventDefault()
        const token = localStorage.getItem('token');

        let url = process.env.REACT_APP_BACK_URL + 'rooms';
        axios.post(
            url, {
                'name': this.state.room_name,
                'duration_seconds': Number(this.state.duration) * 60,
                'min_start_time': this.state.start_time + '+03:00',
                'max_start_time': this.state.end_time + '+03:00'
            }, {
                headers: {
                    Authorization: 'Bearer ' + token
                }
            }
        ).then(_ => {
        }).catch(function (_) {
        })
    }

    render() {
        if (!this.state.is_root) {
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
                    <div className='question-main'>
                        <h1 className='question-label'>Доступ запрещён</h1>
                        <span>У вас нет доступа до создания комнаты. Если вы хотите получить такую возможность, нажмите на кнопку ниже, тогда вашу заявку рассмотрит администратор.</span>
                        <button className='submit-answer-button' onClick={this.submitForm}>Заказать доступ</button>
                    </div>
                </>
            )
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
                    <div className='wide-element'>
                        <h1 className='room-main-label'>Комнаты</h1>
                    </div>
                    <div className='wide-element'>
                        <div className='room-list'>
                            {this.genRoomsList()}
                        </div>
                    </div>
                    <div className='wide-element'>
                        <h1 className='room-main-label'>Создать комнату</h1>
                    </div>
                    <div className='wide-element'>
                        <form onSubmit={this.handleSubmit} onChange={this.handleChange} className='create-room-form'>
                            <div className='room-form-splitter'>
                                <span>Имя команты</span>
                                <input type='text' placeholder='Название' />
                            </div>
                            <div className='room-form-splitter'>
                                <span>Длительность</span>
                                <input type='number' placeholder='Минуты' min='1' max='1440' />
                            </div>
                            <div className='room-form-splitter'>
                                <span>Минимальное время начала</span>
                                <input type="datetime-local" />
                            </div>
                            <div className='room-form-splitter'>
                                <span>Максимальное время начала</span>
                                <input type="datetime-local" />
                            </div>
                            <button className='login-button'>Создать</button>
                        </form>
                    </div>
                </div>
            </>
        );
    }
}

export default Room;
