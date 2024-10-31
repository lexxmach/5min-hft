from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    
    credentials = relationship("Credentials", back_populates="user")
    
    
class Credentials(Base):
    __tablename__ = 'credentials'
    credentials_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    login = Column(String)
    password_hash = Column(String)
    
    user = relationship("User", back_populates="credentials")


class QuestionsType(Base):
    __tablename__ = 'question_type'
    question_type_id = Column(Integer, primary_key=True)
    question_type_name = Column(String)
    
    question_type = relationship("Questions", back_populates="question_type")


class Questions(Base):
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True)
    question_type_id = Column(Integer, ForeignKey('question_type.question_type_id'))
    question = Column(String)
    answer = Column(String)
    
    question_type = relationship("QuestionsType", back_populates="question_type_id")