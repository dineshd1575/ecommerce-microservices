import os

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL', 'sqlite:////data/orders.db'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
PRODUCT_SERVICE_URL = os.environ.get(
    'PRODUCT_SERVICE_URL', 'http://product_management:5000'
)
