# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

# Create the database instance (without initializing it)
# This will be imported and initialized in app.py

from database import db
# Import models for easy access
from .menu import MenuItem, Recipe
from .orders import Order, OrderItem
from .stock import Ingredient
from .branch import Branch
from .associations import menu_item_branches