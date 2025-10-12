from fastapi import FastAPI, Depends
import uvicorn
from pydantic import BaseModel 
from routers import default_router, users_router, quizes_router, question_router
from contextlib import asynccontextmanager
from database import DataRepository as dr


@asynccontextmanager
async def lifespan(app:FastAPI):
    await dr.create_table()
    await dr.add_test_data()
    print('-------------Bases build---------------')

    yield #генератор на паузе
    await dr.delete_table()
    print('------------------Bases dropped---------------')


app = FastAPI(lifespan=lifespan)

app.include_router(default_router)   #подключаем роутеры, д.б. APIRouters
app.include_router(quizes_router)
app.include_router(users_router)
app.include_router(question_router)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

