from flask import Flask, jsonify, request
from models import db, Product
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

jwt = JWTManager(app)


@app.route('/products', methods=['POST']) # Create
@jwt_required()
def create_product():
    data = request.json
    new_product = Product(name=data['name'], description=data.get('description', ''), price=data['price'], quantity=data['quantity'])
    db.session.add(new_product)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Product already exists'}), 409
    return jsonify({'id': new_product.id}), 201

@app.route('/products', methods=['GET']) # Read
@jwt_required()
def get_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'description': p.description, 'price': p.price, 'quantity': p.quantity} for p in products]), 200

@app.route('/products/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price, 'quantity': product.quantity}), 200

@app.route('/products/<int:product_id>', methods=['PUT']) # Update
@jwt_required()
def update_product(product_id):
    data = request.json
    product = Product.query.get_or_404(product_id)
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.quantity = data.get('quantity', product.quantity)
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'}), 200

@app.route('/products/<int:product_id>', methods=['DELETE']) # Delete
@jwt_required()
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'service': 'product_management',
        'status': 'healthy'
    }), 200

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
