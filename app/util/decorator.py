from functools import wraps
from flask import request, g

from app.service.auth_helper import Auth
from app.service.rate_limiter import RateLimiter
from app.service.exception import RateLimitExceededError


def verified_request(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        site_id = kwargs['site_id']

        data, status = Auth.verify_request(request, site_id)
        status = data.get('status')

        if not status or status != "success":
            return data, status

        g.site_details = data

        return f(*args, **kwargs)

    return decorated


def rate_limited_request(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        site_data = g.site_details.get('data')
        remaining_calls = RateLimiter.get_remaining_calls(
            site_data['id'],
            site_data['max_requests'],
            site_data['window_seconds']
        )

        if remaining_calls <= 0:
            raise RateLimitExceededError("Request rate limit reached")

        return f(*args, **kwargs)

    return decorated


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        success = data.get('status')

        if not success or success != "success":
            return data, status

        return f(*args, **kwargs)

    return decorated
