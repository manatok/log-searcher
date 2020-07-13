import time
from flask import current_app
from werkzeug.exceptions import TooManyRequests


class RateLimiter:

    @staticmethod
    def get_remaining_calls(site_id: str, max_calls: int, window_timeframe: int):
        now = time.time_ns() / 1e9

        pipeline = current_app.redis.pipeline()
        pipeline.zrangebyscore(site_id, 0, now - window_timeframe)
        pipeline.zrange(site_id, 0, -1)
        pipeline.zadd(site_id, {now: now})
        pipeline.expire(site_id, window_timeframe)
        result = pipeline.execute()

        return max(0, max_calls - len(result[1]))
