from collections.abc import Generator, Callable

from fastapi import Depends
from sqlalchemy import exc, Engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

from common.repo.repository import DatabaseRepository


def get_db_session_callable(engine: Engine) -> Callable[[], Generator[Session, None]]:
    def func() -> Generator[Session, None]:
        factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        with factory() as session:
            try:
                yield session
                session.commit()
            except exc.SQLAlchemyError:
                session.rollback()
                raise
    return func


def get_repository_callable(engine : Engine) -> Callable[[Session], DatabaseRepository]:
    def get_db_session() -> Generator[Session, None]:
        db_session_func = get_db_session_callable(engine)
        for session in db_session_func():
            yield session
    
    def func(session: Session = Depends(get_db_session)):
        return DatabaseRepository(session)
    return func
