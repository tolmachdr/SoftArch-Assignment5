from typing import Annotated

from fastapi import APIRouter, Depends, Body

from src.service.schemas import TweetSchema
from src.db.base import Session, get_session
from src.api.utils import CURRENT_USER_ID_DEPENDENCY
from src.service.tweet import TweetService

router = APIRouter(prefix="/tweet", tags=["Tweet"])


@router.get("/feed")
def feed(session: Session = Depends(get_session)) -> list[TweetSchema]:
    return TweetService(session=session).get_feed()


@router.post("/publish-tweet")
def publish_tweet(user_id: CURRENT_USER_ID_DEPENDENCY,
                  text: Annotated[str, Body(max_length=400)],
                  session: Session = Depends(get_session)) -> None:
    TweetService(session=session).publish_tweet(author_id=user_id, text=text)


@router.post("/like-tweet")
def like_tweet(user_id: CURRENT_USER_ID_DEPENDENCY,
               tweet_id: Annotated[str, Body()],
               session: Session = Depends(get_session)) -> None:
    TweetService(session=session).like_tweet(user_id=user_id, tweet_id=tweet_id)

