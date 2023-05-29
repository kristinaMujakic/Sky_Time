from app import app
import os
import datetime
from unittest import TestCase

from models import db, User, Location


os.environ['DATABASE_URL'] = "postgresql:///skytime_test"

with app.app_context():
    db.create_all()


class UserModelTestCase(TestCase):
    '''Test Model'''

    def setUp(self):
        '''Set up the test environment.'''

        app.config['TESTING'] = True
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        '''Clean up after each test.'''

        with app.app_context():
            db.drop_all()

    def test_user_model(self):
        '''Test the User model.'''

        with app.app_context():
            user = User.signup(username='testuser', email='test@example.com',
                               password='password', image_url='/static/images/test_img.png')
            db.session.commit()

            self.assertEqual(User.query.count(), 1)
            self.assertEqual(user.username, 'testuser')
            self.assertEqual(user.email, 'test@example.com')
            self.assertEqual(user.image_url, '/static/images/test_img.png')

    def test_authenticate(self):
        '''Test the authenticate method of the User model.'''

        with app.app_context():
            user = User.signup(username='testuser', email='test@example.com',
                               password='password', image_url='/static/images/test_img.png')
            db.session.commit()

            authenticated_user = User.authenticate(
                username='testuser', password='password')
            self.assertEqual(authenticated_user, user)

            authenticated_user = User.authenticate(
                username='testuser', password='wrongpassword')
            self.assertFalse(authenticated_user)

    def test_location_model(self):
        '''Test the Location model.'''

        with app.app_context():
            user = User.signup(username='testuser', email='test@example.com',
                               password='password', image_url='/static/images/test_img.png')
            db.session.commit()

            location = Location(
                user_id=user.username,
                latitude=37.7749,
                longitude=-122.4194,
                city='San Francisco',
                state='CA',
                country='USA',
                date=datetime.date(2023, 5, 26)
            )

            db.session.add(location)
            db.session.commit()

            self.assertEqual(location.date, datetime.date(2023, 5, 26))


if __name__ == '__main__':
    unittest.main()
