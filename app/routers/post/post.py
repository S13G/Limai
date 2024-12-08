from typing import List, Optional

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import count
from starlette import status
from starlette.responses import Response

from app.database.database import get_db
from app.routers.post.models import Post
from app.routers.post.responses import PostResponse, PostOut
from app.routers.post.schemas import PostCreate
from app.routers.vote.models import Vote
from app.utilities import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Post"],
)


@router.get("/", response_model=List[PostOut])
def get_posts(
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user),  # noqa
        limit: int = 10,
        skip: int = 0,
        search: Optional[str] = "",
):
    posts = (  # noqa
        db.query(Post)
        .filter(Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    results = (
        db.query(Post, count(Vote.post_id).label("votes"))
        .join(Vote, Vote.post_id == Post.id, isouter=True)
        .group_by(Post.id)
        .all()
    )
    results = list(map(lambda x: x._mapping, results))  # noqa
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(
        post: PostCreate,
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user),
):
    new_post = Post(owner_id=current_user.id, **post.model_dump())

    db.add(new_post)  # create
    db.commit()  # save to db
    db.refresh(new_post)  # get the new post from db and store back into the variable

    return new_post


@router.get("/{post_id}", response_model=PostResponse)
def get_post(
        post_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user),  # noqa
):
    post = db.query(Post).filter(Post.id == post_id).first()  # noqa

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )

    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
        post_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user),
):
    post_query = db.query(Post).filter(Post.id == post_id)  # noqa

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized to perform requested action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{post_id}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse
)
def update_post(
        post_id: int,
        updated_post: PostCreate,
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user),  # noqa
):
    post_query = db.query(Post).filter(Post.id == post_id)  # noqa

    gotten_post = post_query.first()

    if gotten_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} not found",
        )

    post_query.update(updated_post.model_dump(), synchronize_session=False)

    db.commit()
    return post_query.first()
