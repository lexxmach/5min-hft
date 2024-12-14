import React from "react";
import axios from "axios";
import './profile.css';

class Profile extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: '',
            surname: '',
            solved_by_category: {},
            total_by_category: {},
        };

        this.genStats = this.genStats.bind(this);
    }

    componentDidMount() {
        const token = localStorage.getItem('token');

        let url = 'http://localhost:8000/info/';
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

        url = 'http://localhost:8000/stats/';
        axios.get(url, {
            headers: {
                Authorization: 'Bearer ' + token
            }
        }).then(res => {
            let data = res.data;
            this.setState({
                solved_by_category: data['solved_questions_by_category_count'],
                total_by_category: data['total_questions_by_category_count'],
            })
        });
    }

    genStats() {
        let result = []

        for (let category in this.state.solved_by_category) {
            result.push(
                <div className='stats-item'>
                    <span className='bold'>{category}: </span>
                    <span>{this.state.solved_by_category[category]}</span>
                </div>
            )
        }

        return result
    }

    render() {
        return (
            <>
                <div className='header'>
                        <a href='/' className='header-href'>Меню</a>
                        <a href='/question' className='header-href'>Вопросы</a>
                        <a href='/leaderboard' className='header-href'>Лидерборд</a>
                        <a href='/profile' className='header-href'>{this.state.name}</a>
                    </div>
                <div className='profile-main'>
                    <div className='wide-element'>
                        <h1 className='profile-big-name'>{this.state.name + ' ' + this.state.surname}</h1>
                    </div>
                    <div className='wide-element'>
                        <span>Статистика решенных пользователем задач по категориям:</span>
                    </div>
                    <div className='wide-element'>
                        {this.genStats()}
                    </div>
                </div>
            </>
        );
    }
}

export default Profile;
