from src.db import Tweet, Likes
from src.db.base import Session
from src.service.schemas import TweetSchema

from src.db.repository import TweetRepository, LikesRepository


class TweetService:
    def __init__(self, session: Session):
        self.session = session

    def get_feed(self) -> list[TweetSchema]:
        likes_repo = LikesRepository(session=self.session)
        return [
            TweetSchema.build_from_orm(tweet, likes=likes_repo.get_likes(tweet_id=tweet.id))
            for tweet in TweetRepository(self.session).get_multi()
        ]

    def publish_tweet(self, author_id: str, text: str):
        TweetRepository(self.session).save(Tweet(author_id=author_id, text=text))

    def like_tweet(self, user_id: str, tweet_id: str):
        repo = LikesRepository(self.session)
        if repo.get_by_attr(user_id=user_id, tweet_id=tweet_id) is not None:
            return
        repo.save(Likes(user_id=user_id, tweet_id=tweet_id))
