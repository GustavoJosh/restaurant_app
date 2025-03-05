# models/stock.py
from database import db

class Ingredient(db.Model):
    __tablename__ = 'raw_ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total_quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.Enum("kg", "g", "l", "ml", "piece"), nullable=False)
    recipes = db.relationship('Recipe', backref='ingredient', cascade="all, delete-orphan")
    is_active = db.Column(db.Boolean, default=True, nullable=False)