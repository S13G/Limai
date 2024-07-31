from datetime import datetime

from app.routers.post.schemas import PostBase


class PostResponse(PostBase):
    id: int
    created_at: datetime
