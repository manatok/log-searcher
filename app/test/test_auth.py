import unittest

import json
from app.test.base import BaseTestCase
from app.dataprovider.user_dataprovider import test_users


def login_user(self, email, password):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json'
    )


class TestAuthBlueprint(BaseTestCase):

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            response = login_user(
                self, test_users[0]['email'], test_users[0]['password'])
            data = json.loads(response.data.decode())
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = login_user(self, 'unknown', 'password')
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] ==
                            'Email or password does not match.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
