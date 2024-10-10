from pydantic import BaseModel, Field


class PostTweetRequestSchema(BaseModel):
    text: str = Field(max_length=400)
