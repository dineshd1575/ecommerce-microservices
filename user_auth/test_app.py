import unittest
from app import app, db
from models import User


class UserAuthTestCase(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            JWT_SECRET_KEY='test-only-secret-key-for-ci-pipeline-123456789',
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )

        self.context = app.app_context()
        self.context.push()

        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def test_register_user(self):
        response = self.client.post(
            '/register',
            json={'username': 'test1', 'password': 'test1'}
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.query.count(), 1)

    def test_login_user(self):
        self.client.post(
            '/register',
            json={'username': 'test1', 'password': 'test1'}
        )

        response = self.client.post(
            '/login',
            json={'username': 'test1', 'password': 'test1'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)


if __name__ == '__main__':
    unittest.main()
