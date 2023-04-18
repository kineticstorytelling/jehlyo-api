from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Product, product_schema, products_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'Work': 'now'}

@api.route('/products', methods = ['POST'])
@token_required
def create_car(current_user_token):
    name = request.json['name']
    cost = request.json['cost']
    store = request.json['store']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    product = Product(name, cost, store, user_token=user_token)

    db.session.add(product)
    db.session.commit()

    response = product_schema.dump(product)
    return jsonify(response)

@api.route('/products', methods = ['GET'])
@token_required
def get_car(current_user_token):
    a_user = current_user_token.token
    products = Product.query.filter_by(user_token = a_user).all()
    response = products_schema.dump(products)
    return jsonify(response)

@api.route('/products/<id>', methods = ['GET'])
@token_required
def get_single_product(current_user_token, id):
    product = Product.query.get(id)
    response = product_schema.dump(product)
    return jsonify(response)


@api.route('/products/<id>', methods = ['POST', 'PUT'])
@token_required
def update_product(current_user_token, id):
    product = Product.query.get(id)
    product.name = request.json['name']
    product.cost = request.json['cost']
    product.store = request.json['store']
    product.user_token = current_user_token.token

    db.session.commit()
    response = product_schema.dump(product)
    return jsonify(response)

#Delete route
@api.route('/products/<id>', methods = ['DELETE'])
@token_required
def delete_product(current_user_token, id):
    product=Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    response = product_schema.dump(product)
    return jsonify(response)