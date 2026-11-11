import unittest
from app import app, db
from models import Order
import requests_mock

class OrderProcessingTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_orders.db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_order(self):
        with requests_mock.Mocker() as m:
            m.get('http://product_management:5001/products/1', json={'id': 1, 'quantity': 10}, status_code=200)
            m.put('http://product_management:5001/products/1', json={'quantity': 9}, status_code=200)

            response = self.app.post('/orders', json={'product_id': 1, 'quantity': 1})
            self.assertEqual(response.status_code, 201)
            self.assertEqual(Order.query.count(), 1)

    # Can add more tests here...

if __name__ == '__main__':
    unittest.main()
