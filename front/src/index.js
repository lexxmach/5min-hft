import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { AnimatedBackground } from 'animated-backgrounds';
import Main from './urls/main/main.js';
import Login from './urls/login/login.js';
import Register from './urls/register/register.js';
import Question from './urls/question/question.js';
import Profile from './urls/profile/profile.js';
import Leaderboard from './urls/leaderboard/leaderboard.js';
import Room from './urls/room/room.js';
import CreateQuestion from './urls/create/question/create_question.js';
import ExamQuestion from './urls/exam_sessions/question/question.js'
import Start from './urls/exam_sessions/start/start.js'
import Results from './urls/exam_sessions/results/results.js'
import { BrowserRouter, Route, Routes } from "react-router-dom";
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <>
    <AnimatedBackground animationName="geometricShapes" />
    <BrowserRouter>
        <Routes>
            <Route path='/' element={<Main />} />
            <Route path='/login' element={<Login />} />
            <Route path='/register' element={<Register />} />
            <Route path='/question' element={<Question />} />
            <Route path='/profile' element={<Profile />} />
            <Route path='/leaderboard' element={<Leaderboard />} />
            <Route path='/rooms' element={<Room />} />
            <Route path='/create/question' element={<CreateQuestion />} />
            <Route path='/exam_sessions/question' element={<ExamQuestion />} />
            <Route path='/exam_sessions/start' element={<Start />} />
            <Route path='/exam_sessions/results' element={<Results />} />
        </Routes>
    </BrowserRouter>
  </>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
