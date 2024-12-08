from datetime import datetime

from pydantic import BaseModel

from app.routers.core.responses import UserOut
from app.routers.post.schemas import PostBase


class PostResponse(PostBase):
    id: int
    owner_id: int
    owner: UserOut
    created_at: datetime


class PostOut(BaseModel):
    Post: PostResponse
    votes: int
