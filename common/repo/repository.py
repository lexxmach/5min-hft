from typing import Any, Generic, TypeVar

from sqlalchemy import BinaryExpression, select, delete, update
from sqlalchemy.orm import Session, DeclarativeBase


Model = TypeVar("Model", bound=DeclarativeBase)

class DatabaseRepository(Generic[Model]):
    def __init__(self, session: Session) -> None:
        self.session = session


    def create(self, data: dict, model: type[Model]) -> Model:
        instance = model(**data)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance
    

    def update(self, *expressions: BinaryExpression, data: dict[str, Any], model: type[Model]) -> None:
        query = update(model).where(*expressions).values(**data)
        self.session.execute(query)
        self.session.commit()


    def delete(self, *expressions: BinaryExpression, model: type[Model]) -> None:
        query = delete(model).where(*expressions)
        self.session.execute(query)
        self.session.commit()

        
    def filter(self, *expressions: BinaryExpression, model: type[Model], order_by = None) -> list[Model]:
        query = select(model)
        if expressions:
            query = query.where(*expressions)
        if order_by is not None:
            query = query.order_by(order_by)
        return list(self.session.scalars(query))