from typing import Optional

from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
