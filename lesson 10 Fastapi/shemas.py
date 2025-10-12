from pydantic import BaseModel, ConfigDict

#отдельные схемы для юзеров(объектов ORM) для работы с фаст: из ORM в пайдентик

class UserADD(BaseModel): #юзер приходит и отправляется
    name:str
    age:int
    phone:str | None = None

class User(UserADD): #отправляется юзер
    id:int
    model_config = ConfigDict(from_attributes=True)  #берет данные из любого объекта с атрибутами т.е. Pydantic мог создавать свою модель из объекта SQLAlchemy, а не только из словаря

class UserID(BaseModel): #схема для ответа
    id: int

class QuizAdd(BaseModel):
    name:str
    user_id:int

class Quiz(QuizAdd):
    id:int
    model_config = ConfigDict(from_attributes=True)

class QuizId(BaseModel):
    id:int

class QuestionAdd(BaseModel):
    text:str
    answer:str
    wrong:str

class Question(QuestionAdd):
    id:int
    model_config = ConfigDict(from_attributes=True)

class QuestionId(BaseModel):
    id:int

class QuizQuestion(Quiz):
    questions:list['Question']     

QuizQuestion.model_rebuild()


class QuizLinkQuestions(BaseModel):
    questions_id:list[int]

    
