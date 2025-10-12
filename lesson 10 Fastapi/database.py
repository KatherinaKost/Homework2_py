#Обертка для БД

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import select, insert
from models import UserORM, Model, QuizOrm, QuestionOrm, quiz_question
from shemas import *
import os

BASE_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(BASE_DIR, 'db')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

DB_PATH = os.path.join(DB_DIR, 'fastapi.db')

engine = create_async_engine(f'sqlite+aiosqlite:///{DB_PATH}') #aiosqlite асинхронный инпут оутпут
""" (engine) — специальный объект, через который приложение связывается с базой данных """

#фабрика сессий, для открытия сессий в нужный момент
new_session = async_sessionmaker(engine, expire_on_commit=False)
""" 'expire_on_commit=False' не отключает ORM-объекты после сохранения, чтобы  спокойно их возвращать из API """

#репозитории для работы с объектами со всеми функциями для работы (например во Flask прописывали функции сразу в эндпоинтах)

class UserRepository:
    @classmethod
    async def add_user(cls, user:UserADD) -> int: #берем юзера из схемы
        async with new_session() as session:
            data = user.model_dump() #данные в виде словаря 
            print(data)
            user = UserORM(**data) #создали объект ОРМ
            session.add(user)
            await session.flush() #попытка предварительной записи
            await session.commit() #пользователь сохранился в БД
            return user.id 
        
    @classmethod
    async def get_users(cls) -> list[UserORM]:
        async with new_session() as session:
            query = select(UserORM) #Выбрать все записи из таблицы, связанной с моделью UserORM - создать запрос
            res = await session.execute(query) #выполнить запрос
            users = res.scalars().all() #получили список 
            return users
        
    @classmethod
    async def get_user(cls, id) -> list[UserORM]:
        async with new_session() as session:
            query = select(UserORM).filter(UserORM.id==id) #Выбрать юзера по айди - создать запрос
            #query = text('SQL')
            res = await session.execute(query) #выполнить запрос
            user = res.scalars().first() #получили объект юзера
            return user

class QuizRepository:
    @classmethod
    async def add_quiz(cls, quiz:QuizAdd): #берется из падэнтика
        async with new_session() as session:
            data = quiz.model_dump() #данные в виде словаря 
            print(data)
            quiz = QuizOrm(**data) #создали объект ОРМ
            session.add(quiz)  
            await session.flush() #попытка предварительной записи
            await session.commit() #пользователь сохранился в БД
            return quiz.id 

    @classmethod   
    async def get_quiz(cls, id) -> QuizOrm:
        async with new_session() as session:
            query = select(QuizOrm).filter(QuizOrm.id==id)
            res = await session.execute(query)
            quiz = res.scalars().first()
            return quiz
        
    @classmethod   
    async def get_quizes(cls) -> list[QuizOrm]:
        async with new_session() as session:
            query = select(QuizOrm)
            res = await session.execute(query)
            quizes = res.scalars().all()
            return quizes
        
    @classmethod
    async def get_quizes_question(cls, id:int):
        """ Как сделать чтобы код не дублировался и в запросе на сам квиз по айди и в получении вопросов?????????????? """
        async with new_session() as session:
            query = select(QuizOrm).filter(QuizOrm.id==id)        
            res = await session.execute(query)
            quiz = res.scalars().first()
            await session.refresh(quiz, ['questions']) 
            return quiz
        
    """ session.refresh(...) - Перезагружает данные объекта из БД 
        quiz - ORM-объект, который должен быть в текущей сессии
        ['questions'] - Список атрибутов (обычно relationship), которые нужно загрузить/обновить
        ИНАЧЕ ОШИБКА С Lazy load"""
    
    @classmethod
    async def link_quiz_question(cls, id:int, questions_id:QuizLinkQuestions):
        async with new_session() as session:
            query = select(QuizOrm).filter(QuizOrm.id==id)        
            res = await session.execute(query)
            quiz = res.scalars().first()
            quiz_id = quiz.id
            res = [{"quiz_id": quiz_id, "question_id": question_id} for question_id in questions_id.questions_id]
            
            stmt = insert(quiz_question).prefix_with("OR IGNORE")   
            """ stmt = insert(...).prefix_with("OR IGNORE") - Готовит  команду вставки, которая не падает на дублях, 
                благодаря .prefix_with("OR IGNORE")
                await session.execute(stmt, res) - Выполняет  данными """
            
            await session.execute(stmt, res)
            await session.commit()
       
class QuestionRepository:
    @classmethod
    async def add_question(cls, question:QuestionAdd):
        async with new_session() as session:
            data = question.model_dump()
            question = QuestionOrm(**data)
            session.add(question)
            await session.flush()
            await session.commit()
            return question.id

    @classmethod
    async def get_questions(cls) -> list[QuestionOrm]:
        async with new_session() as session:
            query = select(QuestionOrm)
            res = await session.execute(query)
            questions = res.scalars().all()
            return questions
        
    @classmethod
    async def get_question(cls, id) -> QuestionOrm:
        async with new_session() as session:
            query = select(QuestionOrm).filter(QuestionOrm.id==id)
            res = await session.execute(query)
            question = res.scalars().first()
            return question


class  DataRepository:
    @classmethod
    async def create_table(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.create_all)
    
    @classmethod            
    async def delete_table(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.drop_all)     

    @classmethod
    async def add_test_data(cls):
        async with new_session() as session:
            users = [
                UserORM(name='user1', age=20),
                UserORM(name='user2', age=30, phone='123456789'),
                UserORM(name='user3', age=41, phone='11'),
            ]
            session.add_all(users)
            await session.flush()

            quizes = [
                QuizOrm(name='quiz1', user_id=users[0].id),
                QuizOrm(name='quiz2', user_id=users[1].id),
                QuizOrm(name='quiz3', user_id=users[2].id),
            ]
            session.add_all(quizes)
            await session.flush()

            questions = [
                QuestionOrm(text='Скульптура «Медный всадник» посвящена', answer='Петру великому', wrong='Александру III'),
                QuestionOrm(text='С дневнегреческого "синий камень" переводится как:', answer='Сапфир', wrong='луна'),
                QuestionOrm(text='Как называется «детектор лжи»?', answer='полиграф', wrong='полиндром'),
                QuestionOrm(text='Орхидея - национальный цветок какой страны?', answer='Тайланд', wrong='Китай'),
                QuestionOrm(text='Каллисто и ИО спутники:', answer='Юпитера', wrong='Сатурна'),
                QuestionOrm(text='Сколько жизней у кошек', answer='9', wrong='10')
            ]
            session.add_all(questions)
            await session.flush()

            

            
            quiz_question_data = [
                {"quiz_id": quizes[0].id, "question_id": questions[0].id},
                {"quiz_id": quizes[0].id, "question_id": questions[1].id},
                {"quiz_id": quizes[0].id, "question_id": questions[2].id},
                {"quiz_id": quizes[1].id, "question_id": questions[2].id},
                {"quiz_id": quizes[1].id, "question_id": questions[3].id},
                {"quiz_id": quizes[1].id, "question_id": questions[4].id},
                {"quiz_id": quizes[2].id, "question_id": questions[4].id},
                {"quiz_id": quizes[2].id, "question_id": questions[5].id},
            ]
            await session.execute(insert(quiz_question), quiz_question_data)

            await session.commit()
            
            
            
            
            
                    
            
            # flush() - используется для синхронизации изменений с базой данных без завершения транзакции
            # проверяет, что операции (вставка, обновление) не вызывают ошибок
            # Если последующие действия в транзакции зависят от предыдущих изменений, 
            # flush() делает эти изменения видимыми в рамках текущей сессии
            
            