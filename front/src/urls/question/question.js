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
            answer: '',
            current_ans: '',
            state: 0
        };

        this.onAnswer = this.onAnswer.bind(this);
    }

    componentDidMount() {
        let url = 'http://localhost:8000/questions/';
        axios.get(url).then(res => {
            let data = res.data;
            this.setState({
                dataLoaded: true,
                question: data['question'],
                answer: data['answer'],
                state: 0
            })
        });
    }

    onAnswer(e) {
        e.preventDefault();
        if (this.state.answer === this.state.current_ans) {
            this.setState({state: 1})
        } else {
            this.setState({state: 2})
        }
    }

    getPanel() {
        if (this.state.state === 0) {
            return (
                <>
                    <div className='wide-element'>
                        <input className='question-answer' type='text' placeholder='Ваш ответ' onChange={event => this.setState({current_ans: event.target.value})} />
                    </div>
                    <button className='question-button' onClick={this.onAnswer}>Проверить ответ</button>
                </>
            )
        }
        if (this.state.state === 1) {
            return (
                <>
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
                    <div className='wide-element'>
                        <span className='wrong-answer'>Ответ неправильный!</span>
                    </div>
                    <div className='wide-element'>
                        <span className='right-answer'>Правильный ответ: {this.state.answer}</span>
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
                <div className='question-main'>
                    <h1 className='question-label'>Ответьте на вопрос:</h1>
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
            );
        } else {
            return (
                <div className='question-main'>
                    <h1 className='question-label'>Ответьте на вопрос:</h1>
                    <span>Загрузка...</span>
                    <input className='question-answer' type='text' placeholder='Ваш ответ' />
                    <button className='question-button'>Проверить ответ</button>
                </div>
            );
        }
    }
}

export default Question;
