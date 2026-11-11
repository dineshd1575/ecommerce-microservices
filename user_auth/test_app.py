import unittest
from app import app, db
from models import User

class UserAuthTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_users.db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user(self):
        response = self.app.post('/register', json={'username': 'test1', 'password': 'test1'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.query.count(), 1)

    def test_login_user(self):
        self.app.post('/register', json={'username': 'test1', 'password': 'test1'})
        response = self.app.post('/login', json={'username': 'test1', 'password': 'test1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    # Can add more tests here...

if __name__ == '__main__':
    unittest.main()
