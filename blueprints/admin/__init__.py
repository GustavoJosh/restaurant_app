# blueprints/admin/__init__.py
from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Import routes to register them with the blueprint
from . import menu_routes, ingredient_routes, recipe_routes, order_routes, branch_routes