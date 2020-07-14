import unittest
import requests
import time
import urllib.parse


class LogAPITests(unittest.TestCase):
    """
    Some crude smoke tests to make sure that a user can post logs,
    login and query the logs. These tests will fail if Elasticsearch
    is not up yet.
    """

    log_url = 'http://0.0.0.0:5000/api/v1/logs/site1'

    def test_run_all_in_sequence(self):
        """
        Ensure that the tests are all run in the correct order
        """
        self.add_logs()
        time.sleep(5)
        self.query_logs()
        self.rate_limit()

    def add_logs(self):
        """
        Ensure that a log message can be added successfully
        """
        header = {
            "Content-type": "application/json",
            "Referer": "http://localhost"
        }
        payload = {"message": "This is a test log"}
        response = requests.post(self.log_url, json=payload, headers=header)
        assert response.status_code == 201

    def rate_limit(self):
        """
        Ensure that the rate limiting takes effect
        """
        header = {
            "Content-type": "application/json",
            "Referer": "http://localhost"
        }

        for i in range(9):
            payload = {"message": "This is a test log"}
            response = requests.post(
                self.log_url, json=payload, headers=header)
            assert response.status_code == 201

        payload = {"message": "This is a test log"}
        response = requests.post(self.log_url, json=payload, headers=header)
        assert response.status_code == 429

    def query_logs(self):
        """
        Ensure that the log created is found when performing a basic search
        """
        access_token = self.get_access_token()
        header = {"Authorization": access_token}
        query = "message contains 'test'"
        url = self.log_url + '?query=' + urllib.parse.quote(query)
        response = requests.get(url, headers=header)

        assert response.status_code == 200
        json_response = response.json()
        print("Got response: ", json_response)
        expected_response = {'data': [{'message': 'This is a test log', 'browser': 'python-requests/2.24.0',
                                       'url': 'http://localhost', 'country': 'Not found'}]}

        assert json_response == expected_response

    def get_access_token(self):
        """
        Ensure that an access token can be generated
        """
        email = "site1@test.com"
        password = "test"
        login_url = 'http://0.0.0.0:5000/api/v1/auth/login'
        payload = {"email": email, "password": password}
        header = {"Content-type": "application/json"}
        response = requests.post(login_url, json=payload, headers=header)

        assert response.status_code == 200
        json_response = response.json()
        assert 'Authorization' in json_response

        return json_response['Authorization']


if __name__ == '__main__':
    unittest.main()
