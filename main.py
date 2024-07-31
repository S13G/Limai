import time

import psycopg2
from decouple import config
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

from app.database.database import engine, Base
from app.routers.core import user, auth
from app.routers.post import post

Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            host=config('DATABASE_HOST'),
            database=config('DATABASE_NAME'),
            user=config('DATABASE_USER'),
            password=config('DATABASE_PASSWORD'),
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        break
    except Exception as error:
        print('Database connection error')
        print('Error: ', error)
        time.sleep(2)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
