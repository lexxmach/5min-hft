from datetime import datetime
from pydantic import ValidationError
from models.enums import QuestionType
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.schemas import UserAnswer
from models.models import Answers, AnswersMultipleOptions, History, Questions

def get_question_by_user_id(db: Session, user_id: int) -> tuple[Questions, list[str]]:
    subquery = db.query(History.question_id).filter(History.user_id == user_id).subquery()
    question = db.query(Questions).filter(~Questions.id.in_(subquery)).first()

    if not question:
        return None, None

    answer_options = None
    if question.type == QuestionType.TEXT:
        answer_options = None
    elif question.type == QuestionType.ORDER:
        answer_options = db.query(Answers).filter(Answers.question_id == question.id).all()
        answer_options = [answer_option.answer_text for answer_option in answer_options]
    elif question.type == QuestionType.CHECKBOX or question.type == QuestionType.RADIO:
        answer_options = db.query(AnswersMultipleOptions).filter(AnswersMultipleOptions.question_id == question.id).all()
        answer_options = [answer_option.option_text for answer_option in answer_options]
    else:
        return None, None
    
    return question, answer_options


def create_history_entry(db: Session, user_answer: UserAnswer) -> History:
    question = db.query(Questions).filter(Questions.id == user_answer.question_id).first()
    if not question:
       return None
   
    is_correct = False

    if question.type == QuestionType.TEXT:
        answer = db.query(Answers).filter(Answers.question_id == question.id).first()
        if len(user_answer.users_answer) == 1:
            is_correct = answer.answer_text == user_answer.users_answer[0]
    elif question.type == QuestionType.ORDER:
        correct_answers = db.query(Answers).filter(Answers.question_id == question.id).order_by(Answers.order_position).all()
        correct_answers = [correct_answer.answer_text for correct_answer in correct_answers]
        if len(user_answer.users_answer) == len(correct_answers):
            is_correct = True
            for given_answer, correct_answer in zip(user_answer.users_answer, correct_answers):
                if given_answer != correct_answer:
                    is_correct = False
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
        user_id=user_answer.user_id,
        question_id=user_answer.question_id,
        users_answer=user_answer.users_answer,
        correctly_answered=is_correct,
        timestamp=datetime.now()
    )
    db.add(history_entry)
    db.commit()
    return history_entry