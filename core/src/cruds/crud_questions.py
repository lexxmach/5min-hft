from datetime import datetime
from pydantic import ValidationError
from common.repo.repository import DatabaseRepository
from models.enums import QuestionType
from sqlalchemy import and_, func

from models.schemas import SubmitNewQuestion, UserAnswer, QuestionRequest
from models.models import Answers, AnswersMultipleOptions, History, Questions

import random

def create_question(repo: DatabaseRepository, new_question: SubmitNewQuestion) -> Questions:
    try:
        db_question = {"text": new_question.question_text, "type": new_question.type, 
                       "difficulty": new_question.difficulty, "category": new_question.category, 
                       "hint": new_question.hint}
        db_question = repo.create(db_question, model=Questions)
        db_answer = None
        if new_question.answer:
            db_answer = {"question_id": db_question.id, "answer_text": new_question.answer.answer_text}

        db_options = []
        if new_question.answers_multiple_options:
            for option in new_question.answers_multiple_options:
                db_option = {
                    "question_id": db_question.id,
                    "option_text": option.option_text,
                    "is_correct": option.is_correct}
                
                db_options.append(db_option)
    except ValidationError:
        return None
    
    if db_answer:
        repo.create(db_answer, model=Answers)
    elif db_options:
        for db_option in db_options:
            repo.create(db_option, model=AnswersMultipleOptions)
    return db_question
    

def get_question_by_id(repo: DatabaseRepository, question_id: int) -> tuple[Questions, list[str]]:
    question = repo.filter(Questions.id == question_id, model=Questions)
    if not question:
        return None, None, None
    question = question[0]
    
    correct_answers = None
    answers = None
    if question.type == QuestionType.TEXT:
        correct_answers = [repo.filter(Answers.question_id == question.id, model=Answers)[0].answer_text]
        answers = [repo.filter(Answers.question_id == question.id, model=Answers)[0].answer_text]
    elif question.type == QuestionType.CHECKBOX or question.type == QuestionType.RADIO:
        correct_answers = repo.filter(and_(AnswersMultipleOptions.question_id == question.id, AnswersMultipleOptions.is_correct == True), model=AnswersMultipleOptions)
        correct_answers = [answer_option.option_text for answer_option in correct_answers]
        answers = repo.filter(AnswersMultipleOptions.question_id == question.id, model=AnswersMultipleOptions)
        answers = [answer_option.option_text for answer_option in answers]
    else:
        return None, None, None
    
    return question, correct_answers, answers


def get_question_by_parameters(repo: DatabaseRepository, user_id: int, request: QuestionRequest) -> tuple[Questions, list[str] | None]:
        subquery = repo.session.query(History.question_id).filter(and_(History.user_id == user_id, History.correctly_answered == True)).subquery()
        
        filters = [~Questions.id.in_(subquery)]
        if request.type is not None:
            filters.append(Questions.type == request.type)
        if request.difficulty is not None:
            filters.append(Questions.difficulty == request.difficulty)
        if request.category is not None:
            filters.append(Questions.category == request.category)
        
        if filters:
            query = repo.filter(and_(*filters), model=Questions)
        else:
            query = repo.filter(model=Questions)
        question = query
        
        if len(question) == 0:
            return None, None
        
        question = random.choice(question)
        
        answer_options = None
        if question.type == QuestionType.TEXT:
            answer_options = None
        elif question.type == QuestionType.CHECKBOX or question.type == QuestionType.RADIO:
            answer_options = repo.filter(AnswersMultipleOptions.question_id == question.id, model=AnswersMultipleOptions)
            answer_options = [answer_option.option_text for answer_option in answer_options]
        else:
            return None, None
        
        return question, answer_options
    

def create_history_entry(repo: DatabaseRepository, user_id: int, user_answer: UserAnswer) -> History:
    question = repo.filter(Questions.id == user_answer.question_id, model=Questions)
    if not question:
       return None
    question = question[0]
    
    is_correct = False
    if question.type == QuestionType.TEXT:
        answer = repo.filter(Answers.question_id == question.id, model=Answers)[0]
        if len(user_answer.users_answer) == 1:
            formatted_user_answer = user_answer.users_answer[0].strip().lower()
            formatted_correct_answer = answer.answer_text.strip().lower()
            is_correct = (formatted_correct_answer == formatted_user_answer)
    elif question.type == QuestionType.CHECKBOX or question.type == QuestionType.RADIO:
        correct_answers = repo.filter(and_(AnswersMultipleOptions.question_id == question.id, AnswersMultipleOptions.is_correct == True), model=AnswersMultipleOptions).all()
        correct_answers = [correct_answer.option_text for correct_answer in correct_answers]
        if len(user_answer.users_answer) == len(correct_answers):
            is_correct = True
            for given_answer, correct_answer in zip(sorted(user_answer.users_answer), sorted(correct_answers)):
                if given_answer != correct_answer:
                    is_correct = False
    else:
        return None, None
    
    history_entry = {
        "user_id": user_id,
        "question_id": question.id,
        "users_answer": " ".join(user_answer.users_answer),
        "correctly_answered": is_correct,
        "timestamp": datetime.now()
        }
    
    return repo.create(history_entry, model=History)


def clear_history_for_user(repo: DatabaseRepository, user_id: int) -> int:
    number = len(repo.filter(History.user_id == user_id, model=History))
    repo.delete(History.user_id == user_id, model=History)
    return number


def get_solved_question_by_user(repo: DatabaseRepository, user_id: int) -> dict[str, int]:
    questions = repo.session.query(Questions.category,func.count(func.distinct(Questions.id)).label("unique_id_count")).join(History).filter(and_(History.user_id == user_id, History.correctly_answered == True)).group_by(Questions.category).all()
    categories = repo.filter(model=Questions)
    
    solved_questions_by_category_count = {}
    for category in categories:
        solved_questions_by_category_count[category.category] = 0
    
    for solved_question in questions:
        solved_questions_by_category_count[solved_question.category] = solved_question.unique_id_count
        
    return solved_questions_by_category_count


def get_total_question_by_category(repo: DatabaseRepository) -> dict[str, int]:
    questions = repo.session.query(Questions.category,func.count(func.distinct(Questions.id)).label("unique_id_count")).group_by(Questions.category).all()
    categories = repo.filter(model=Questions)
    
    total_question_by_category = {}
    for category in categories:
        total_question_by_category[category.category] = 0
    
    for solved_question in questions:
        total_question_by_category[solved_question.category] = solved_question.unique_id_count
        
    return total_question_by_category