
import datetime
from ..config import key
import jwt


test_users = [
    {
        "id": 1,
        "email": "site1@test.com",
        "password": "test",
        "allowed_site_ids": ["site1", "site11"]
    },
    {
        "id": 2,
        "email": "site2@test.com",
        "password": "test",
        "allowed_site_ids": ["site2", "site22"]
    }
]


class User:
    id = None
    email = None
    password = None
    allowed_site_ids = []

    def __init__(self, id: str, email: str, password: str, allowed_site_ids: [str]):
        self.id = id
        self.email = email
        self.password = password
        self.allowed_site_ids = allowed_site_ids

    @staticmethod
    def get_by(column: str, value: str):
        for user in test_users:
            if user[column] == value:
                return User(user["id"], user["email"], user["password"],
                            user["allowed_site_ids"])

        return None

    def check_password(self, password):
        return password == self.password

    def encode_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': {
                    'id': self.id,
                    'site_ids': self.allowed_site_ids
                }
            }

            return jwt.encode(payload, key, algorithm='HS256')

        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: string
        :raise jwt.ExpiredSignatureError
        :raise jwt.InvalidTokenError
        """
        payload = jwt.decode(auth_token, key)
        return payload['sub']
