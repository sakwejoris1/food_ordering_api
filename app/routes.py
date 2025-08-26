from flask import Blueprint, request, jsonify
from .models import Fruit, CartItem, Order, OrderItem
from . import db

main = Blueprint('main', __name__)

@main.route('/fruit', methods=['GET'])
def get_fruits():
    fruits = Fruit.query.all()
    return jsonify([{'id': f.id, 'name': f.name, 'price': f.price} for f in fruits])

# -----------------------
# Add item to cart
# -----------------------
@main.route('/cart', methods=['POST'])
def add_cart_item():
    data = request.get_json()
    fruit_id = data.get('fruit_id')
    quantity = data.get('quantity', 1)

    fruit = Fruit.query.get(fruit_id)
    if not fruit:
        return jsonify({'error': 'Fruit not found'}), 404

    cart_item = CartItem(fruit_id=fruit_id, quantity=quantity)
    db.session.add(cart_item)
    db.session.commit()

    return jsonify({'id': cart_item.id, 'fruit_id': cart_item.fruit_id, 'quantity': cart_item.quantity}), 201

# -----------------------
# View cart
# -----------------------
@main.route('/cart', methods=['GET'])
def view_cart():
    cart = CartItem.query.all()
    output = []
    for item in cart:
        output.append({
            'id': item.id,
            'fruit': item.fruit.name,
            'quantity': item.quantity,
            'total': item.quantity * item.fruit.price
        })
    return jsonify(output)

# -----------------------
# Update cart item quantity
# -----------------------
@main.route('/cart/<int:item_id>', methods=['PUT'])
def update_cart_item(item_id):
    data = request.get_json()
    item = CartItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    item.quantity = data.get('quantity', item.quantity)
    db.session.commit()
    return jsonify({'message': 'Cart item updated'})

# -----------------------
# Delete cart item
# -----------------------
@main.route('/cart/<int:item_id>', methods=['DELETE'])
def delete_cart_item(item_id):
    item = CartItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'}), 200

# -----------------------
# Place order
# -----------------------
@main.route('/orders', methods=['POST'])
def place_order():
    cart_items = CartItem.query.all()
    if not cart_items:
        return jsonify({'error': 'Your cart is empty'}), 400

    # Create a new order
    order = Order(status="Pending")
    db.session.add(order)
    db.session.commit()  # Commit once to get order.id

    # Create OrderItems
    order_items = []
    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            fruit_id=cart_item.fruit_id,
            quantity=cart_item.quantity
        )
        order_items.append(order_item)
        db.session.add(order_item)

    # Clear cart
    for cart_item in cart_items:
        db.session.delete(cart_item)

    db.session.commit()  # Commit all changes at once

    return jsonify({
        'message': 'Order placed successfully',
        'order_id': order.id,
        'status': order.status
    }), 201

# -----------------------
# Get all orders
# -----------------------
@main.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    output = []

    for order in orders:
        items = []
        for item in order.items:
            items.append({
                'fruit_id': item.fruit_id,
                'quantity': item.quantity,
                'price': item.fruit.price
            })

        order_data = {
            'id': order.id,
            'status': order.status,
            'created_at': order.created_at,
            'items': items
        }
        output.append(order_data)

    return jsonify(output)
