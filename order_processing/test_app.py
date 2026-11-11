import unittest
from app import app, db
from models import Order
from flask_jwt_extended import create_access_token
import requests_mock


class OrderProcessingTestCase(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            JWT_SECRET_KEY='test-only-secret-key-for-ci-pipeline',
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )

        self.context = app.app_context()
        self.context.push()

        db.create_all()
        self.client = app.test_client()

        token = create_access_token(identity='test-user')

        self.headers = {
            'Authorization': f'Bearer {token}'
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def test_create_order(self):
        with requests_mock.Mocker() as m:

            m.get(
                'http://product_management:5000/products/1',
                json={'id': 1, 'quantity': 10},
                status_code=200
            )

            m.put(
                'http://product_management:5000/products/1',
                json={'quantity': 9},
                status_code=200
            )

            response = self.client.post(
                '/orders',
                headers=self.headers,
                json={'product_id': 1, 'quantity': 1}
            )

            self.assertEqual(response.status_code, 201)
            self.assertEqual(Order.query.count(), 1)


if __name__ == '__main__':
    unittest.main()
