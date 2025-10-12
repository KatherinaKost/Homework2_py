#создается модель пользователя ORM
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Table, Column, func

class Model(DeclarativeBase): #класс для создания структуры таблицы
    pass

quiz_question = Table('quiz_question',
                      Model.metadata,
                      Column('quiz_id', ForeignKey('quizes.id'), primary_key=True),
                      Column('question_id', ForeignKey('questions.id'), primary_key=True)
                      )

class UserORM(Model): #отдельный класс для юзера из бд
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True) #mapped_column задаёт параметры столбца: тип, первичный ключ, уникальность и т.д.
    name: Mapped[str]
    age: Mapped[int]
    phone: Mapped[str|None]
    quiz = relationship('QuizOrm', backref='user')

class QuizOrm(Model):
    __tablename__ = 'quizes'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    

class QuestionOrm(Model):
    __tablename__ = 'questions'
    id:Mapped[int] = mapped_column(primary_key=True)
    text:Mapped[str] = mapped_column(nullable=False)
    answer:Mapped[str] = mapped_column(nullable=False)
    wrong:Mapped[str] = mapped_column(nullable=False)
    quizes = relationship('QuizOrm', secondary=quiz_question, backref='questions')