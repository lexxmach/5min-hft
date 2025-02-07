import React from "react";
import './question.css';
import { TypeAnimation } from 'react-type-animation';
import axios from "axios";


class Question extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            dataLoaded: false,
            question: '',
            current_ans: [],
            state: 0,
            question_id: 0,
            difficulty: 0,
            category: 'unknown',
            type: '',
            options: [],
            hint: '',
        };

        this.onAnswer = this.onAnswer.bind(this);
        this.getCheckboxes = this.getCheckboxes.bind(this);
        this.onChangeCheckbox = this.onChangeCheckbox.bind(this);
        this.getRadio = this.getRadio.bind(this);
        this.onChangeRadio = this.onChangeRadio.bind(this);
        this.getInput = this.getInput.bind(this);
    }

    componentDidMount() {
        const token = localStorage.getItem('token');

        const queryParameters = new URLSearchParams(window.location.search)
        const id = queryParameters.get("id")

        let url = 'http://localhost:8000/questions/';

        if (id !== null) {
            url = 'http://localhost:8000/questions/by-id?question_id=' + id;
        }

        axios.get(url, {
            headers: {
                Authorization: 'Bearer ' + token
            }
        }).then(res => {
            let data = res.data;
            this.setState({
                dataLoaded: true,
                question: data['question'],
                state: 0,
                question_id: data['id'],
                difficulty: data['difficulty'],
                category: data['category'],
                type: data['type'],
                options: data['options'],
                hint: data['hint'],
                name: '',
                surname: '',
            })
        });

        url = 'http://localhost:8000/info/';
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

    onAnswer(e) {
        e.preventDefault();
        const token = localStorage.getItem('token');

        let url = 'http://localhost:8000/questions/submit-answer';
        axios.post(url, {
            'user_id': 1,
            'question_id': this.state.question_id,
            'users_answer': this.state.current_ans
        }, {
            headers: {
                Authorization: 'Bearer ' + token
            }
        }).then(res => {
            let data = res.data;
            if (data['is_answer_correct']) {
                this.setState({state: 1})
            } else {
                this.setState({state: 2})
            }
        });
    }

    onChangeCheckbox(event) {
        if (this.state.current_ans.includes(event.target.value)) {
            let index = this.state.current_ans.findIndex(item => item == event.target.value);
            this.state.current_ans.splice(index, 1);
        } else {
            this.setState({current_ans: this.state.current_ans.concat([event.target.value])})
        }
    }

    onChangeRadio(event) {
        this.setState({current_ans: [event.target.value]})
    }

    getCheckboxes() {
        let result = []
        for (var i = 0; i < this.state.options.length; i++) {
            result.push(
                <div className='option'>
                    <span>
                        <input
                            className='question-answer-checkbox'
                            type='checkbox'
                            value={this.state.options[i]}
                            onChange={this.onChangeCheckbox}
                        />
                        {this.state.options[i]}
                    </span>
                </div>
            )
        };
        return result
    }

    getRadio() {
        let result = []
        for (var i = 0; i < this.state.options.length; i++) {
            result.push(
                <div className='option'>
                    <span>
                        <input
                            className='question-answer-radio'
                            type='radio'
                            name='ans'
                            value={this.state.options[i]}
                            onChange={this.onChangeRadio}
                        />
                        {this.state.options[i]}
                    </span>
                </div>
            )
        };
        return result
    }

    getInput() {
        if (this.state.type == 'TEXT') {
            return (
                <div className='wide-element'>
                    <input className='question-answer' type='text' placeholder='Ваш ответ' onChange={event => this.setState({current_ans: [event.target.value]})} />
                </div>
            )
        } else if (this.state.type == 'CHECKBOX') {
            return (
                <div className='options-grid'>
                    {this.getCheckboxes()}
                </div>
            )
        } else if (this.state.type == 'RADIO') {
            return (
                <div className='options-grid'>
                    {this.getRadio()}
                </div>
            )
        }
    }

    getPanel() {
        if (this.state.state === 0) {
            return (
                <>
                    {this.getInput()}
                    <button className='question-button' onClick={this.onAnswer}>Проверить ответ</button>
                </>
            )
        }
        if (this.state.state === 1) {
            return (
                <>
                    {this.getInput()}
                    <div className='wide-element'>
                        <span className='right-answer'>Ответ правильный</span>
                    </div>
                    <form action="http://localhost:3000/question">
                        <button className='question-button'>Далее</button>
                    </form>
                </>
            )
        }
        if (this.state.state === 2) {
            return (
                <>
                    {this.getInput()}
                    <div className='wide-element'>
                        <span className='wrong-answer'>Ответ неправильный!</span>
                    </div>
                    <div className='wide-element'>
                        <span>Мы ещё покажем этот вопрос позже, а пока можете ознакомиться с подсказкой</span>
                    </div>
                    <div className='wide-element'>
                        <span>Подсказка: {this.state.hint}</span>
                    </div>
                    <form action="http://localhost:3000/question">
                        <button className='question-button'>Далее</button>
                    </form>
                </>
            )
        }
    }

    render() {
        if (this.state.dataLoaded) {
            return (
                <>
                    <div className='header'>
                        <a href='/' className='header-href'>Меню</a>
                        <a href='/question' className='header-href'>Вопросы</a>
                        <a href='/leaderboard' className='header-href'>Лидерборд</a>
                        <a href='/create/question' className='header-href'>Создать</a>
                        <a href='/profile' className='header-href'>{this.state.name}</a>
                    </div>
                    <div className='question-main'>
                        <h1 className='question-label'>Воспрос №{this.state.question_id}:</h1>
                        <div className='wide-element'>
                            <div className='splitter'>
                                <span className='question-info'>Сложность: {this.state.difficulty}</span>
                                <span className='question-info'>Категория: {this.state.category}</span>
                            </div>
                        </div>
                        <div className='wide-element'>
                            <TypeAnimation
                                sequence={[
                                    this.state.question
                                ]}
                                wrapper="span"
                                speed={100}
                                cursor={false}
                                style={{
                                    display: 'block',
                                }}
                            />
                        </div>
                        {this.getPanel()}
                    </div>
                </>
            );
        } else {
            return (
                <div className='question-main'>
                    <h1 className='question-label'>Загрузка...</h1>
                    <span>Загрузка...</span>
                </div>
            );
        }
    }
}

export default Question;
