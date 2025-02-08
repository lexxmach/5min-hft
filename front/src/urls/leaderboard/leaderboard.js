import React from "react";
import axios from "axios";
import './leaderboard.css';

class Leaderboard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            sorted_users_by_category: {},
        };

        this.genLeaderboard = this.genLeaderboard.bind(this);
        this.genCategoryLeaderboard = this.genCategoryLeaderboard.bind(this);
    }

    componentDidMount() {
        const token = localStorage.getItem('token');

        let url = process.env.REACT_APP_BACK_URL + '/info/';
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

        url = process.env.REACT_APP_BACK_URL + 'leaderboard/';
        axios.get(url, {
            headers: {
                Authorization: 'Bearer ' + token
            }
        }).then(res => {
            let data = res.data;
            this.setState({
                sorted_users_by_category: data['sorted_users_by_category'],
            })
        });
    }

    genCategoryLeaderboard(category) {
        let result = []

        for (let i = 0; i < this.state.sorted_users_by_category[category].length; ++i) {
            result.push(
                <div className='leaderboard-person'>
                    <div className='leaderboard-person-number'>
                        <span>{i + 1}.</span>
                        <span className='bold'>{this.state.sorted_users_by_category[category][i].name} {this.state.sorted_users_by_category[category][i].surname}</span>
                    </div>
                    <span>{this.state.sorted_users_by_category[category][i]['tasks_solved']}</span>
                </div>
            )
        }

        return result
    }

    genLeaderboard() {
        let result = []

        for (let category in this.state.sorted_users_by_category) {
            result.push(
                <div className='leaderboard'>
                    <h2 className='leaderboard-label'>{category}</h2>
                    {this.genCategoryLeaderboard(category)}
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
                        <a href='/create/question' className='header-href'>Создать</a>
                        <a href='/profile' className='header-href'>{this.state.name}</a>
                    </div>
                <div className='leaderboar-main'>
                    <div className='wide-element'>
                        <h1 className='leaderboard-main-label'>Лидерборд</h1>
                    </div>
                    <div className='wide-element'>
                        <span>Лидерборд пользователей по количеству решённых задач по каждой из категории</span>
                    </div>
                    <div className='wide-element'>
                        {this.genLeaderboard()}
                    </div>
                </div>
            </>
        );
    }
}

export default Leaderboard;
