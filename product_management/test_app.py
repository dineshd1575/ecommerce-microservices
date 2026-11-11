import unittest
from app import app, db
from models import Product
from flask_jwt_extended import create_access_token

class ProductManagementTestCase(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            JWT_SECRET_KEY='test-only-secret-key-for-ci-pipeline-123456789',
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

    def test_create_product(self):
        response = self.client.post(
            '/products',
            headers=self.headers,
            json={
                'name': 'Test Product',
                'description': 'Test Description',
                'price': 10.0,
                'quantity': 100
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.query.count(), 1)

    def test_get_product(self):
        response = self.client.post(
            '/products',
            headers=self.headers,
            json={
                'name': 'Test Product',
                'description': 'Test Description',
                'price': 10.0,
                'quantity': 100
            }
        )

        self.assertEqual(response.status_code, 201)

        response = self.client.get(
            '/products/1',
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Test Product')

if __name__ == '__main__':
    unittest.main()
