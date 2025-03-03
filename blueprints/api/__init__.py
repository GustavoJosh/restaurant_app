# blueprints/admin/__init__.py
from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')
    

# Import routes to register them with the blueprint
from . import api_routes