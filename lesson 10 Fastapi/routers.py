#дефолтный роутер - главный роутер
from fastapi import APIRouter, Depends, HTTPException, status
from database import UserRepository as ur, QuestionRepository as quesr, QuizRepository as quizr
from shemas import *

default_router = APIRouter()  

users_router = APIRouter(     #каждый роутер как отдельный объект
    prefix='/users',
    tags=['Пользователи']
) 

quizes_router = APIRouter(
    prefix='/quizes',
    tags=['Квизы']
)

question_router = APIRouter(
    prefix='/questions',
    tags=['Вопросы']
)

@default_router.get('/', tags=['Api'])
async def index():
    return {'data':'ok'}

""" -----------------------------Роутеры для юзеров--------------------------------------------- """
@users_router.get('')       #сюда ничего не пишем, так как ранее указали
async def users_get() :
    users = await ur.get_users()  #Берем из репозитория
    if not users:
        raise HTTPException(status_code=404, detail="Пользователи не найдены")
    return users


@users_router.get('/{id}')       
async def user_get(id:int) -> User:
    user = await ur.get_user(id)  #Берем из репозитория
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user
""" создается объект на основании другого объекта из-за ConfigDict в схемах """


@users_router.post('')
async def add_user(user:UserADD = Depends()) -> UserID:
    try:
        id = await ur.add_user(user)
        return {'id':id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="ошибка сервера")
""" ------------------------------------------------------------------------------------------------ """
""" ----------------------------------Роутеры для квизов-------------------------------------------- """
@quizes_router.get('')
async def quizes_get() -> list[Quiz]:     #получаем квизы все
    quizes = await quizr.get_quizes()
    if not quizes:
        raise HTTPException(status_code=404, detail="Квизы не найдены")
    return quizes

@quizes_router.get('/{id}') #квиз по айди
async def quiz_get(id:int) -> Quiz:
    quiz = await quizr.get_quiz(id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Квиз не найден")
    return quiz

@quizes_router.post('')
async def add_quiz(quiz:QuizAdd=Depends()) -> QuizId:
    try:
        id = await quizr.add_quiz(quiz)
        return{'id':id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="ошибка сервера")

@quizes_router.get('/{id}/questions')
async def quiz_questions_get(id:int) -> QuizQuestion:
    quiz = await quizr.get_quizes_question(id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Квиз не найден")
    return quiz

@quizes_router.post('/{id}/link')
async def quiz_question_link(id:int, data:QuizLinkQuestions):
    try:
        await quizr.link_quiz_question(id, data)
        return {
                "quiz_id": id,
                "linked_question_ids": data.questions_id, 
                }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Любая другая непредвиденная ошибка
        raise HTTPException(status_code=500, detail="ошибка сервера")
""" ------------------------------------------------------------------------------------------------- """
""" ---------------------------------Роутеры для вопросов-------------------------------------------- """
@question_router.get('')
async def questions_get() -> list[Question]:     #получаем вопросы все
    questions = await quesr.get_questions()
    if not questions:
        raise HTTPException(status_code=404, detail="Вопросы не найдены")
    return questions

@question_router.get('/{id}') #вопрос по айди
async def questions_get(id:int) -> Question:
    question = await quesr.get_question(id)
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    return question

@question_router.post('')
async def add_question(question:QuestionAdd = Depends()) -> QuestionId:
    try:
        id = await quesr.add_question(question)
        return{'id':id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="ошибка сервера")
    



