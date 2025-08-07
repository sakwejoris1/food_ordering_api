from .import db
from datetime import datetime


class fruit(db.Model):
    id = db.Column(db.Interger, primary_key=True)
    name = db.Column(db.string(100), nullable=False)
    price = db.Column(db.float, nullable=False)

class CartItem(db.Model):
    id = db.Column(db.Interger, primary_key=True)
    fruit_id = db.Column(db.Interger, db.ForeignKey('fruit.id'), nullable=False)
    quantity = db.Column(db.Interger, nullable=False)

    fruit = db.relationship('fruit')
class order(db.Model):
    id = db.Column(db.Interger, primary_key=True)
    created_at = db.Column(db.Datetime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order')

class OrderItem(db.Model):
    id = db.Column(db.Interger), primary_key=True
    order_id = db.Column(db.Interger, db.ForeignKey('order.id'))
    quantity = db.Column(db.Interger)
    price = db.Column(db.float)

 

