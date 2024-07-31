from datetime import datetime

from app.routers.core.responses import UserOut
from app.routers.post.schemas import PostBase


class PostResponse(PostBase):
    id: int
    owner: UserOut
    created_at: datetime
