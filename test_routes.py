import os
from unittest import TestCase
from app import app
from models import db

os.environ['DATABASE_URL'] = "postgresql:///skytime_test_2"

with app.app_context():
    db.create_all()


class RoutesTestCase(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def tearDown(self):
        with app.app_context():
            db.session.rollback()
            db.drop_all()

    def test_homepage(self):
        '''Test homepage route'''
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Sky Time', response.data)

    def test_signup(self):
        '''Test signup route'''
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Unlock the wonders of Sky Time today and sign up!', response.data)


if __name__ == '__main__':
    unittest.main()
