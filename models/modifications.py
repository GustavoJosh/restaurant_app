# models/modifications.py
from database import db

# New model for tracking modifications
class OrderItemModification(db.Model):
    __tablename__ = 'order_item_modifications'
    id = db.Column(db.Integer, primary_key=True)
    order_item_id = db.Column(db.Integer, db.ForeignKey("order_items.id", ondelete="CASCADE"), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("raw_ingredients.id"), nullable=False)
    
    # Type: add (extra), remove, substitute
    modification_type = db.Column(db.Enum("add", "remove", "substitute"), nullable=False)
    
    # For "add" and "substitute" - how much to add
    quantity = db.Column(db.Float, default=1.0)
    
    # Only for "substitute" type
    replacement_ingredient_id = db.Column(db.Integer, db.ForeignKey("raw_ingredients.id"), nullable=True)
    
    # Price adjustment (+ for additions, 0 for removals unless premium item)
    price_adjustment = db.Column(db.Float, default=0.0)
    
    # Relationships
    order_item = db.relationship("OrderItem", backref="modifications")
    ingredient = db.relationship("Ingredient", foreign_keys=[ingredient_id])
    replacement = db.relationship("Ingredient", foreign_keys=[replacement_ingredient_id])