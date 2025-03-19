from models.enums import QuestionType
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base

class Questions(Base):
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    type = Column(Enum(QuestionType), nullable=False)
    difficulty = Column(Integer, default=1)
    category = Column(String)
    hint = Column(String)

    answers = relationship('Answers', back_populates='question', cascade='all, delete')
    answers_multiple_options = relationship('AnswersMultipleOptions', back_populates='question', cascade='all, delete')
    history = relationship('History', back_populates='question', cascade='all, delete')


class Answers(Base):
    __tablename__ = 'answers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    answer_text = Column(String)

    question = relationship('Questions', back_populates='answers')

class AnswersMultipleOptions(Base):
    __tablename__ = 'answersmultipleoptions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    option_text = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)

    question = relationship('Questions', back_populates='answers_multiple_options')

class UserData(Base):
    __tablename__ = 'userdata'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    is_root = Column(Boolean, nullable=False)

    credentials = relationship('Credentials', back_populates='userdata', cascade='all, delete')
    history = relationship('History', back_populates='userdata', cascade='all, delete')

class Credentials(Base):
    __tablename__ = 'credentials'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('userdata.id', ondelete='CASCADE'), nullable=False)
    login = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)

    userdata = relationship('UserData', back_populates='credentials')

class History(Base):
    __tablename__ = 'history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('userdata.id', ondelete='CASCADE'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    users_answer = Column(String)
    correctly_answered = Column(Boolean)
    timestamp = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')

    userdata = relationship('UserData', back_populates='history')
    question = relationship('Questions', back_populates='history')


class Rooms(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("userdata.id", ondelete="CASCADE"))
    
    owner = relationship("UserData")
    questions = relationship("QuestionsInRoom", back_populates="rooms")


class QuestionsInRoom(Base):
    __tablename__ = "questionsinroom"
    
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), primary_key=True)
    
    rooms = relationship("Rooms", back_populates="questions")
    question = relationship("Questions")