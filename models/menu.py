# models/menu.py
from models import db

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)  # Soft deletion flag

    #  Relationship with Recipes
    recipes = db.relationship('Recipe', backref='menu_item', cascade="all, delete-orphan")

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id', ondelete="CASCADE"), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('raw_ingredients.id', ondelete="CASCADE"), nullable=False)
    quantity_used = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=False)