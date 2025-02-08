import React from "react";
import './create_question.css';
import { Navigate } from "react-router-dom";
import axios from "axios";


class CreateQuestion extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            dataLoaded: false,
            question: '',
            current_ans: '',
            difficulty: 0,
            category: '',
            type: '',
            options: [],
            type: 'TEXT',
            inputs: [],
            redirect_to: -1,
            is_root: false,
        };

        this.getCheckboxes = this.getCheckboxes.bind(this);
        this.onChangeCheckbox = this.onChangeCheckbox.bind(this);
        this.onChangeInput = this.onChangeInput.bind(this);
        this.getRadio = this.getRadio.bind(this);
        this.onChangeRadio = this.onChangeRadio.bind(this);
        this.getInput = this.getInput.bind(this);
        this.submitQuestion = this.submitQuestion.bind(this);
        this.submitForm = this.submitForm.bind(this);
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
    }

    onChangeCheckbox(event) {
        let new_options = this.state.options
        new_options[event.target.value].is_correct = !new_options[event.target.value].is_correct
        this.setState({options: new_options})
    }

    onChangeRadio(event) {
        let new_options = this.state.options
        new_options[event.target.value].is_correct = !new_options[event.target.value].is_correct
        this.setState({options: new_options})
    }

    onChangeInput(event) {
        let new_options = this.state.options
        new_options[event.target.size - 20].option_text = event.target.value
        this.setState({options: new_options})
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
                            value={i}
                            onChange={this.onChangeCheckbox}
                        />
                        <input className='options-input' type='text' size={20 + i} onChange={event => this.onChangeInput(event)} />
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
                            value={i}
                            onChange={this.onChangeRadio}
                        />
                        <input className='options-input' type='text' size={20 + i} onChange={event => this.onChangeInput(event)} />
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
                    <input className='question-answer' type='text' placeholder='Правильный ответ' onChange={event => this.setState({current_ans: event.target.value})} />
                </div>
            )
        } else if (this.state.type == 'CHECKBOX') {
            return (
                <div className='wide-element'>
                    <div className='options-grid'>
                        {this.getCheckboxes()}
                    </div>
                    <div className='splitter'>
                        <button className='question-button-splitted-2x-green' onClick={_ => this.setState({options: this.state.options.concat([{option_text: '', is_correct: false}])})} >Добавить вариант</button>
                        <button className='question-button-splitted-2x-blue' onClick={_ => this.setState({options: this.state.options.slice(0, -1)})} >Убрать вариант</button>
                    </div>
                </div>
            )
        } else if (this.state.type == 'RADIO') {
            return (
                <div className='wide-element'>
                    <div className='options-grid'>
                        {this.getRadio()}
                    </div>
                    <div className='splitter'>
                        <button className='question-button-splitted-2x-green' onClick={_ => this.setState({options: this.state.options.concat([{option_text: '', is_correct: false}])})} >Добавить вариант</button>
                        <button className='question-button-splitted-2x-blue' onClick={_ => this.setState({options: this.state.options.slice(0, -1)})} >Убрать вариант</button>
                    </div>
                </div>
            )
        }
    }

    submitQuestion() {
        const token = localStorage.getItem('token');

        let url = process.env.REACT_APP_BACK_URL + 'questions/new';
        let answer = null
        let options = null
        if (this.state.type === 'TEXT') {
            answer = {
                'answer_text': this.state.current_ans
            }
        } else {
            options = this.state.options
        }
        axios.post(url, {
            'question_text': this.state.question,
            'type': this.state.type,
            'difficulty': Number(this.state.difficulty),
            'category': this.state.theme,
            'hint': '',
            'answer': answer,
            'answers_multiple_options': options
        }, {
            headers: {
                Authorization: 'Bearer ' + token
            }
        }).then(res => {
            this.setState({redirect_to: res.data})
        });
    }

    submitForm() {
        const token = localStorage.getItem('token');

        let url = process.env.REACT_APP_BACK_URL + 'admin/request-access';
        axios.post(url, {}, {
            headers: {
                Authorization: 'Bearer ' + token
            }
        }).then(res => {
            this.setState({redirect_to: -2})
        });
    }

    render() {
        if (this.state.redirect_to === -2) {
            return (
                <Navigate to={'/'} />
            )
        }
        if (this.state.redirect_to !== -1) {
            console.log(this.state.redirect_to)
            return (
                <Navigate to={'/question?id=' + this.state.redirect_to.toString()} />
            )
        }
        if (!this.state.is_root) {
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
                        <h1 className='question-label'>Доступ запрещён</h1>
                        <span>У вас нет доступа до создания вопросов. Если вы хотите получить такую возможность, нажмите на кнопку ниже, тогда вашу заявку рассмотрит администратор.</span>
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
                    <a href='/profile' className='header-href'>{this.state.name}</a>
                </div>
                <div className='question-main'>
                    <h1 className='question-label'>Создать вопрос</h1>
                    <div className='wide-element'>
                        <div className='splitter'>
                            <input className='question-splitted-input' type='text' placeholder='Сложность' onChange={event => this.setState({difficulty: event.target.value})} />
                            <input className='question-splitted-input' type='text' placeholder='Тема' onChange={event => this.setState({theme: event.target.value})} />
                        </div>
                        <input className='question-answer' type='text' placeholder='Текст вопроса' onChange={event => this.setState({question: event.target.value})} />
                        <h1>Тип вопроса:</h1>
                        <div className='splitter'>
                            <button className='question-button-splitted' onClick={_ => this.setState({type: 'TEXT'})} >Текст</button>
                            <button className='question-button-splitted' onClick={_ => this.setState({type: 'CHECKBOX'})} >Чекбокс</button>
                            <button className='question-button-splitted' onClick={_ => this.setState({type: 'RADIO'})} >Радио</button>
                        </div>
                    </div>
                    {this.getInput()}
                    <button className='submit-answer-button' onClick={this.submitQuestion}>Создать</button>
                </div>
            </>
        );
    }
}

export default CreateQuestion;
