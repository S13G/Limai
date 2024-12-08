from pydantic import BaseModel, conint


class VoteSchema(BaseModel):
    post_id: int
    dir: conint(le=1)  # less than or equal to one
