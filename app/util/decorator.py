from functools import wraps
from flask import request, g
from werkzeug.exceptions import TooManyRequests

from app.service.auth_helper import decode_auth_token, verify_log_request, \
    enforce_site_access
from app.service.rate_limiter import RateLimiter


def verified_account(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        """
        Ensure that the request has a Referer and that this
        matches that account set up for the site_id.

        :raises werkzeug.exceptions.Unauthorized: On missing account
            or incorrect Referrer
        """
        g.site = _get_site(kwargs, request)

        return f(*args, **kwargs)

    return decorated


def rate_limited(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        """
        Ensure that the account/site does not exceed the configured
        number of requests per timeframe.

        :raises werkzeug.exceptions.TooManyRequests: When exceeding the limits
        """
        if not g.site:
            g.site = _get_site(kwargs, request)

        remaining_calls = RateLimiter.get_remaining_calls(
            g.site.id,
            g.site.max_requests,
            g.site.window_seconds
        )

        if remaining_calls <= 0:
            raise TooManyRequests("Request rate limit reached")

        return f(*args, **kwargs)

    return decorated


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        """
        If there is a token and it can be decoded then allow the
        request to proceed.

        :raises werkzeug.exceptions.Unauthorized: On expired signature or
            invalid token
        """
        g.token_data = decode_auth_token(request.headers.get('Authorization'))

        return f(*args, **kwargs)

    return decorated


def site_restricted(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        """
        Ensure that the user has access to the logs of this site.

        :raises werkzeug.exceptions.Unauthorized: On expired signature or
            invalid token
        """
        if not g.token_data:
            g.token_data = decode_auth_token(
                request.headers.get('Authorization'))

        enforce_site_access(kwargs['site_id'], g.token_data)

        return f(*args, **kwargs)

    return decorated


def _get_site(kwargs, request):
    site_id = kwargs['site_id']
    referrer = request.headers.get("Referer")
    return verify_log_request(site_id, referrer)
