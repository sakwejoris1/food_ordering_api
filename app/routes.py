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

@main.route('/order')
def view_cart():
    cart = CartItem.query.all()
    output = []
    for item in cart:
        output.append({
            'id' : item.id,
            fruit : item.fruit.name,
            'quantity': item.quantity,
            'total' : item.quantity * item.fruit.price 
        })
    return jsonify(output)


@main.route('/cart/int:item_id', methods=['DELETE'])
def update_cart_item(item_id):
    data = request.get_json()
    item = CartItem.query.get(item_id)

    if not item:
        return jsonify({'error' : 'item not found'}), 404
    
    item.quantity = data.get('quantity' , item.quantity)
    db.session.commit()

    return jsonify({'message' : 'cart item updated'})

@main.route('/cart/<int:item_id>', methods=['DELTE'])
def delete_cart_item(item_id):
    item = CartItem.query.get(item_id)

    if not item:
        return jsonify({'error': 'Item not found'}),404
    
    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'Item deleted successfully'}), 200

@main.route('place_order', methods=['POST'])
def place_order():
    cart_item = CartItem.query.all()
    if not cart_item:
        return jsonify({'error': 'Cart is empty'}), 400
    
    total_price = 0
    for item in cart_item:
        total_price += item.quantity * item.fruit.price


    new_order = Order(total_price=total_price )
    db.session.add(new_order)
    db.session.commit()


    for item in cart_item:
        order_item = OrderItem(
            order_id = new_order.id,
            fruit_it= item.fruit_id,
            quantity = item.quantity
        )

        CartItem.query.delete()
        db.sessio.commit()

        return jsonify({
            'message': 'Order placed successfully',
            'order_id': new_order.id,
            'total_price': total_price
        }), 201
    

@main.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    output = []

    for order in orders:
        items = []
        for item in order.items:
            items.appemd({
                'fruit_id': item.fruit_id,
                'quantity': item.quantity,
                'price': item.price
            })

            order_data = {
            'id': order.id,
            'created_at': order.created_at,
            'items': items
            }