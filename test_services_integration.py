import unittest
import requests

class IntegrationTestCase(unittest.TestCase):

    def test_order_creation(self):
        # Register a new user
        user_response = requests.post('http://localhost:5000/register', json={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(user_response.status_code, 201)

        # Log in as the new user
        login_response = requests.post('http://localhost:5000/login', json={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json()['access_token']

        # Create a new product
        product_response = requests.post('http://localhost:5001/products', json={'name': 'Test Product', 'description': 'Test Description', 'price': 10.0, 'quantity': 5})
        self.assertEqual(product_response.status_code, 201)

        # Create a new order
        order_response = requests.post('http://localhost:5002/orders', headers={'Authorization': f'Bearer {token}'}, json={'product_id': 1, 'quantity': 2})
        self.assertEqual(order_response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
