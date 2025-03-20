from enum import Enum


class QuestionType(Enum):
    TEXT = "TEXT"
    CHECKBOX = "CHECKBOX"
    RADIO = "RADIO"


class QuestionStatusType(Enum):
    INCORRECT = "INCORRECT"
    CORRECT = "CORRECT"
    NOT_ANSWERED = "NOT_ANSWERED"