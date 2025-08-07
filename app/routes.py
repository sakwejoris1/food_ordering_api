from flask import Blueprint, jsonify, request
from .models import fruit , CartItem, Order, OrderItem
from .import db

main = Blueprint('main', __name__)

@main.route('/fruit', methods=['GET'])
def get_fruits():
    fruit = fruit.query.all()
    return jsonify([{'id': f.id, 'name': f.name, 'price': f.price} for f in fruit])

@main.route('/cart', methods=['POST'])
def get_cart_items():
    data = request.get_json()
    fruit_id = data.get('fruit_id')
    quantity = data.get('quantity', 1)

    fruit = fruit.query.get(fruit_id)
    if not fruit:
        return jsonify({'error': 'Fruit not found'}) , 404
    
    cart_item = CartItem(fruit_id = fruit_id, quantity=quantity)
    db.session.add(cart_item)
    db.session.commit()

    return jsonify({'id': cart_item.id, 'fruit_id': cart_item.fruit_id, 'quantity': cart_item.quantity}), 201

