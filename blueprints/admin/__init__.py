# blueprints/admin/__init__.py
from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Move imports below the Blueprint creation
# Import routes AFTER blueprint is defined
from . import menu_routes, ingredient_routes, recipe_routes, branch_routes
# Import order_routes last to avoid circular import
from . import order_routes