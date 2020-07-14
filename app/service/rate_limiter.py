import time
from flask import current_app


class RateLimiter:

    @staticmethod
    def get_remaining_calls(site_id: str, max_calls: int, window_timeframe: int):
        """
        Check how many more API requests the given site is allowed.

        :param str site_id: The site making the request
        :param int max_calls: The maximum number of calls allowed by this site
        :param int window_timeframe: The timeframe that the max appllies to,
            in seconds

        :returns int: The remaining number of allowed calls
        """
        now = time.time_ns() / 1e9

        # start a transaction
        pipeline = current_app.redis.pipeline()
        # remove records added before current window
        pipeline.zrangebyscore(site_id, 0, now - window_timeframe)
        # get a list of all request timestamps in current window
        pipeline.zrange(site_id, 0, -1)
        # add the current request timestamp
        pipeline.zadd(site_id, {now: now})
        # set a new expiry on the list
        pipeline.expire(site_id, window_timeframe)
        # run as atomic transaction
        result = pipeline.execute()

        return max(0, max_calls - len(result[1]))
