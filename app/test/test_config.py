import unittest

from flask import current_app
from flask_testing import TestCase

from app.app import app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'jwt_secret_signing_key')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['REDIS_HOST'] == 'redis')
        self.assertTrue(app.config['REDIS_PORT'] == 6379)
        self.assertTrue(app.config['REDIS_PASSWORD'] == 'password')


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'jwt_secret_signing_key')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['REDIS_HOST'] == 'redis')
        self.assertTrue(app.config['REDIS_PORT'] == 6379)
        self.assertTrue(app.config['REDIS_PASSWORD'] == 'password')


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertFalse(app.config['DEBUG'])


if __name__ == '__main__':
    unittest.main()
