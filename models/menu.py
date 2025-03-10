# models/menu.py
from database import db

# Example structure:
    # {
    #   "additions": [
    #     {"ingredient_id": 5, "name": "Extra Cheese", "price": 10.0, "quantity": 1.0}
    #   ],
    #   "removals": [
    #     {"ingredient_id": 2, "name": "No Onions", "price": 0.0}
    #   ],
    #   "substitutions": [
    #     {"ingredient_id": 3, "replacement_id": 4, "name": "Replace Chicken with Beef", "price": 15.0}
    #   ]
    # }

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)  # Soft deletion flag
    
    # New field for standard modifications
    standard_modifications = db.Column(db.JSON, nullable=True)
    
    #  Relationship with Recipes
    recipes = db.relationship('Recipe', backref='menu_item', cascade="all, delete-orphan")

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id', ondelete="CASCADE"), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('raw_ingredients.id', ondelete="CASCADE"), nullable=False)
    quantity_used = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=False)