from datetime import datetime
from pydantic import ValidationError
from models.enums import QuestionType
from sqlalchemy.orm import Session

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


def create_history_entry(db: Session, answer: UserAnswer) -> History:
    question = db.query(Questions).filter(Questions.id == answer.question_id).first()
    if not question:
       return None

    is_correct = any(
        option.is_correct and option.option_text == answer.users_answer
        for option in question.options
    ) if question.type in ['CHECKBOX', 'RADIO'] else False

    history_entry = History(
        user_id=answer.user_id,
        question_id=answer.question_id,
        users_answer=answer.users_answer,
        correctly_answered=is_correct,
        timestamp=datetime.now()
    )
    db.add(history_entry)
    db.commit()
    return history_entry