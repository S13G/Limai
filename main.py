from fastapi import FastAPI

from app.database.database import engine, Base
from app.routers.core import user, auth
from app.routers.post import post

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
