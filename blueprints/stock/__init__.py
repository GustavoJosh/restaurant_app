# blueprints/stock/__init__.py
from flask import Blueprint

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')

# Import routes AFTER blueprint is defined
from . import stock_routes