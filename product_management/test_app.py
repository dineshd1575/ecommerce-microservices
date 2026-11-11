
import unittest
from app import app, db
from models import Product

class ProductManagementTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_products.db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_product(self):
        response = self.app.post('/products', json={'name': 'Test Product', 'description': 'Test Description', 'price': 10.0, 'quantity': 100})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.query.count(), 1)

    def test_get_product(self):
        self.app.post('/products', json={'name': 'Test Product', 'description': 'Test Description', 'price': 10.0, 'quantity': 100})
        response = self.app.get('/products/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Test Product')

    # Can add more tests here...

if __name__ == '__main__':
    unittest.main()
