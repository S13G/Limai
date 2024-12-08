from sqlalchemy import Column, ForeignKey, Integer

from app.database.database import Base


class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(
        Integer, ForeignKey(column="posts.id", ondelete="CASCADE"), primary_key=True
    )
    user_id = Column(
        Integer, ForeignKey(column="users.id", ondelete="CASCADE"), primary_key=True
    )
