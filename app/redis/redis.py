from redis import Redis
from redis.exceptions import RedisError

from app.core.config import settings


class RedisClient:
    """
    Central Redis client responsible for creating and managing
    the application's Redis connection.
    """

    def __init__(self) -> None:
        self._client = Redis.from_url(
            url=settings.redis.url,
            decode_responses=True,
        )

    @property
    def client(self) -> Redis:
        """
        Returns the Redis client instance.
        """
        return self._client

    def ping(self) -> bool:
        """
        Verify that Redis is reachable.
        """
        try:
            return self._client.ping()
        except RedisError:
            return False

    def close(self) -> None:
        """
        Gracefully closes the Redis connection.
        """
        self._client.close()


redis = RedisClient()