# models/orders.py
from models import db

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(50), default="pending", nullable=False)
    branch_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationship to order items
    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")  #  Allows deleting order & items

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id", ondelete="CASCADE"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    #  Store selected ingredients as a JSON field
    selected_ingredients = db.Column(db.JSON, nullable=True)  # Stores ingredient IDs or names

    #  Relationships
    menu_item = db.relationship("MenuItem", backref="order_items")
