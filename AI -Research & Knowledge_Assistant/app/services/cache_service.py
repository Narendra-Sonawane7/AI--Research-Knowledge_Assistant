import redis
import json


class CacheService:

    def __init__(self):

        try:
            self.redis_client = redis.Redis(
                host="localhost",
                port=6379,
                decode_responses=True
            )

            self.redis_client.ping()
            self.enabled = True

            print("Redis Connected!")

        except Exception:

            self.enabled = False
            print("Redis is NOT running. Cache disabled.")

    def get(self, key):

        if not self.enabled:
            return None

        data = self.redis_client.get(key)

        if data:
            return json.loads(data)

        return None

    def set(
            self,
            key,
            value,
            expiry=3600
    ):

        if not self.enabled:
            return

        self.redis_client.set(
            key,
            json.dumps(value),
            ex=expiry
        )