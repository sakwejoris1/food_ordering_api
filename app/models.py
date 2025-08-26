from . import db
from datetime import datetime


class Fruit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fruit_id = db.Column(db.Integer, db.ForeignKey('fruit.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    fruit = db.relationship('fruit')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order')


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
