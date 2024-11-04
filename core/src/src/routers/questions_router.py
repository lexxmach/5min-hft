from fastapi import Depends, APIRouter

from dependencies import get_db
from src.models.schemas import QuizQuestion
from sqlalchemy.orm import Session
import security
import random

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=QuizQuestion)
def get_question_for_user(db: Session = Depends(get_db)):
    return random.choice([
        QuizQuestion(question="Какая сложность у сортировки пузырьком?", answer="O(n^2)"),
        QuizQuestion(question="Какой метод HTTP используется для создания ресурса?", answer="POST"),
        QuizQuestion(question="Какой алгоритм поиска имеет сложность O(log n)?", answer="Бинарный поиск"),
        QuizQuestion(question="Какой HTTP-метод используется для получения данных с сервера?", answer="GET"),
        QuizQuestion(question="Что означает аббревиатура UX?", answer="User Experience"),
        QuizQuestion(question="Что означает аббревиатура UI?", answer="User Interface"),
        QuizQuestion(question="Какой ключевой показатель используется для оценки успеха?", answer="KPI"),
        QuizQuestion(question="Что обозначает MVP в разработке продукта?", answer="Minimum Viable Product"),
        QuizQuestion(question="Какой язык интерпретируемый: python или c++?", answer="Python"),
        QuizQuestion(question="За сколько работает сортировка слиянием?", answer="O(nlogn)"),
        QuizQuestion(question="Какой тип данных для текста в Python?", answer="str"),
        QuizQuestion(question="Какое ключевое слово для функций в Python?", answer="def"),
        QuizQuestion(question="Какой оператор для условий?", answer="if"),
    ])
