# blueprints/admin/__init__.py
from flask import Blueprint

pos_bp = Blueprint('pos', __name__, url_prefix='/pos')
    

# Import routes to register them with the blueprint
from . import pos_routes