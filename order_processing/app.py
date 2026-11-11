from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from models import db, Order
from config import PRODUCT_SERVICE_URL
import requests

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

jwt = JWTManager(app)

@app.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.json
    product_id = data['product_id']
    quantity = data['quantity']

    # Get the JWT token from the current request
    access_token = request.headers.get('Authorization').split(' ')[1]

    headers = {'Authorization': f'Bearer {access_token}'}
    product_response = requests.get(f'{PRODUCT_SERVICE_URL}/products/{product_id}', headers=headers)

    # Check if the product exists and has enough stock
    if product_response.status_code != 200:
        return jsonify({'message': 'Product not found'}), 404
    product = product_response.json()
    if product['quantity'] < quantity:
        return jsonify({'message': 'Insufficient stock'}), 400

    # Create the order
    new_order = Order(user_id=user_id, product_id=product_id, quantity=quantity)
    db.session.add(new_order)
    db.session.commit()

    # Update the product stock
    updated_stock = product['quantity'] - quantity
    requests.put(f'{PRODUCT_SERVICE_URL}/products/{product_id}', json={'quantity': updated_stock}, headers=headers)

    return jsonify({'id': new_order.id, 'status': new_order.status}), 201

@app.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': order.id, 'product_id': order.product_id, 'quantity': order.quantity, 'status': order.status} for order in orders]), 200


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'service': 'order_processing',
        'status': 'healthy'
    }), 200

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5002)
