import jwt
import datetime
from werkzeug.exceptions import Unauthorized, Forbidden

from app.model.user import User
from app.model.site import Site
from app.model.token_user import TokenUser
from app.dataprovider.user_dataprovider import get_user_by
from app.dataprovider.site_dataprovider import get_site_by_id
from urllib.parse import urlparse
from ..config import key


def encode_auth_token(user: User) -> str:
    """
    Generates the Auth Token with the user credentials
    :return: string
    """
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': {
            'id': user.id,
            'allowed_site_ids': user.allowed_site_ids,
        }
    }

    return jwt.encode(payload, key, algorithm='HS256')


def decode_auth_token(auth_token: str) -> TokenUser:
    """
    Decodes the auth token and return the payload

    :param: auth_token
    :return: TokenUser
    :raises werkzeug.exceptions.Unauthorized: On expired signature or
        invalid token
    """
    try:
        payload = jwt.decode(auth_token, key)

        return TokenUser(
            payload['sub']['id'],
            payload['sub']['allowed_site_ids'])

    except jwt.ExpiredSignatureError:
        raise Unauthorized('Signature expired. Please log in again.')

    except jwt.InvalidTokenError:
        raise Unauthorized('Invalid token. Please log in again.')


def login_user(email: str, password: str) -> str:
    """
    Checks if the login credentials are correct and if they are returns a JWT.

    :returns str: A JWT
    :raises werkzeug.exceptions.Unauthorized: On invalid user
    """
    user = get_user_by('email', email)

    if user and user.check_password(password):
        auth_token = encode_auth_token(user)
        return auth_token.decode()
    else:
        raise Unauthorized('Email or password does not match.')


def verify_log_request(site_id, referrer) -> Site:
    """
    Ensure that the site_id has an account and that the HTTP Referrer
    matches the registered domain.

    :returns Site: On a successful authentication check
    :raises werkzeug.exceptions.Unauthorized: On missing account 
        or incorrect Referrer
    """
    site = get_site_by_id(site_id)

    if not site:
        raise Unauthorized('No account found for site.')

    parsed_uri = urlparse(referrer)

    if parsed_uri.scheme == site.scheme and parsed_uri.netloc == site.domain:
        return site
    else:
        raise Unauthorized('SiteId not registered for this domain.')


def enforce_site_access(site_id: str, token_user: TokenUser):
    """
    Enforce that the user has access to the site.

    :raises werkzeug.exceptions.Forbidden: If the user does not have access
    """
    if site_id not in token_user.allowed_site_ids:
        raise Forbidden()
