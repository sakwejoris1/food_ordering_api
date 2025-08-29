from . import db
from datetime import datetime


class Fruit(db.Model):
    __tablename__ = "fruits"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))


class CartItem(db.Model):
    __tablename__ = "cart_items"
    id = db.Column(db.Integer, primary_key=True)
    fruit_id = db.Column(db.Integer, db.ForeignKey("fruits.id"), nullable=False)

    fruit = db.relationship("Fruit", backref="cart_items")



class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order')


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
