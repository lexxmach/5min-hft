from datetime import datetime
from pydantic import ValidationError
from models.enums import QuestionType
from sqlalchemy.orm import Session
from sqlalchemy import and_, delete, func

from models.schemas import UserAnswer, QuestionRequest
from models.models import Answers, AnswersMultipleOptions, History, Questions

import random

def get_question_by_id(db: Session, question_id: int) -> tuple[Questions, list[str]]:
    question = db.query(Questions).filter(Questions.id == question_id).first()

    if question is None:
        return None, None

    correct_answers = None
    if question.type == QuestionType.TEXT:
        correct_answers = [db.query(Answers).filter(Answers.question_id == question.id).first().answer_text]
    elif question.type == QuestionType.CHECKBOX or question.type == QuestionType.RADIO:
        correct_answers = db.query(AnswersMultipleOptions).filter(and_(AnswersMultipleOptions.question_id == question.id, AnswersMultipleOptions.is_correct == True)).all()
        correct_answers = [answer_option.option_text for answer_option in correct_answers]
    else:
        return None, None
    
    return question, correct_answers


def get_question_by_parameters(db: Session, user_id: int, request: QuestionRequest) -> tuple[Questions, list[str] | None]:
        subquery = db.query(History.question_id).filter(and_(History.user_id == user_id, History.correctly_answered == True)).subquery()
        query = db.query(Questions)
        
        filters = [~Questions.id.in_(subquery)]
        if request.type is not None:
            filters.append(Questions.type == request.type)
        if request.difficulty is not None:
            filters.append(Questions.difficulty == request.difficulty)
        if request.category is not None:
            filters.append(Questions.category == request.category)
        
        if filters:
            query = query.filter(and_(*filters))
        question = query.all()
        
        if len(question) == 0:
            return None, None
        
        question = random.choice(question)
        
        answer_options = None
        if question.type == QuestionType.TEXT:
            answer_options = None
        elif question.type == QuestionType.CHECKBOX or question.type == QuestionType.RADIO:
            answer_options = db.query(AnswersMultipleOptions).filter(AnswersMultipleOptions.question_id == question.id).all()
            answer_options = [answer_option.option_text for answer_option in answer_options]
        else:
            return None, None
        
        return question, answer_options
    

def create_history_entry(db: Session, user_id: int, user_answer: UserAnswer) -> History:
    question = db.query(Questions).filter(Questions.id == user_answer.question_id).first()
    if question is None:
       return None
   
    is_correct = False

    if question.type == QuestionType.TEXT:
        answer = db.query(Answers).filter(Answers.question_id == question.id).first()
        if len(user_answer.users_answer) == 1:
            formatted_user_answer = user_answer.users_answer[0].strip().lower()
            formatted_correct_answer = answer.answer_text.strip().lower()
            is_correct = (formatted_correct_answer == formatted_user_answer)
    elif question.type == QuestionType.CHECKBOX or question.type == QuestionType.RADIO:
        correct_answers = db.query(AnswersMultipleOptions).filter(and_(AnswersMultipleOptions.question_id == question.id, AnswersMultipleOptions.is_correct == True)).all()
        correct_answers = [correct_answer.option_text for correct_answer in correct_answers]
        if len(user_answer.users_answer) == len(correct_answers):
            is_correct = True
            for given_answer, correct_answer in zip(sorted(user_answer.users_answer), sorted(correct_answers)):
                if given_answer != correct_answer:
                    is_correct = False
    else:
        return None, None
    
    history_entry = History(
        user_id=user_id,
        question_id=question.id,
        users_answer=" ".join(user_answer.users_answer),
        correctly_answered=is_correct,
        timestamp=datetime.now()
    )
    db.add(history_entry)
    db.commit()
    return history_entry


def clear_history_for_user(db: Session, user_id: int) -> int:
    number = db.query(History.question_id).filter(History.user_id == user_id).count()
    stmt = delete(History).where(History.user_id == user_id)
    db.execute(stmt)
    db.commit()
    return number

def get_solved_question_by_user(db: Session, user_id: int) -> dict[str, int]:
    questions = db.query(Questions.category,func.count(func.distinct(Questions.id)).label("unique_id_count")).join(History).filter(and_(History.user_id == user_id, History.correctly_answered == True)).group_by(Questions.category).all()
    categories = db.query(Questions.category).all()
    
    solved_questions_by_category_count = {}
    for category in categories:
        solved_questions_by_category_count[category.category] = 0
    
    for solved_question in questions:
        solved_questions_by_category_count[solved_question.category] = solved_question.unique_id_count
        
    return solved_questions_by_category_count


def get_total_question_by_category(db: Session) -> dict[str, int]:
    questions = db.query(Questions.category,func.count(func.distinct(Questions.id)).label("unique_id_count")).group_by(Questions.category).all()
    categories = db.query(Questions.category).all()
    
    total_question_by_category = {}
    for category in categories:
        total_question_by_category[category.category] = 0
    
    for solved_question in questions:
        total_question_by_category[solved_question.category] = solved_question.unique_id_count
        
    return total_question_by_category