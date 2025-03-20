# models/stock_sale.py / Esto es de las ventas del punto cocina
from database import db
from datetime import datetime

class StockSale(db.Model):
    __tablename__ = 'stock_sales'
    id = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('raw_ingredients.id', ondelete="CASCADE"), nullable=False)
    quantity = db.Column(db.Float, nullable=False)  # Amount in kg
    price_per_kg = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id', ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    notes = db.Column(db.String(255), nullable=True)

    # Relationships
    ingredient = db.relationship("Ingredient", backref="stock_sales")
    branch = db.relationship("Branch", backref="stock_purchases")

    def __repr__(self):
        return f"<StockSale {self.id}: {self.quantity}kg of {self.ingredient.name if self.ingredient else 'Unknown'} to {self.branch.name if self.branch else 'Unknown'}>"