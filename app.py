# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort, current_app
from flask_socketio import SocketIO, emit
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime, timezone, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, text
import os
import random
from services import update_stock, update_menu_item_stock
from models.menu import MenuItem, Recipe
from models.orders import Order, OrderItem
from models.stock import Ingredient
from models.branch import Branch
from models.associations import menu_item_branches
# Initialize Flask Extensions
db = SQLAlchemy()
socketio = SocketIO()
migrate = Migrate()
cors = CORS()

# Import services and models

def create_app():
    """Factory function to create and configure the Flask app."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, "templates")
    static_path = os.path.join(base_dir, "static")
    print(f"Template path: {template_path}")
    print(f"Static path: {static_path}")
    
    app = Flask(__name__, template_folder=template_path, static_folder=static_path)
    
    app.secret_key = "PacoWendy2025"

    # Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:PilyRevival25@localhost/restaurant_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Bind Flask App to Extensions
    db.init_app(app)
    socketio.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    
    # Register blueprints
    from blueprints.admin import admin_bp
    from blueprints.api import api_bp
    from blueprints.pos import pos_bp
    
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(pos_bp, url_prefix='/pos')
    
# Create the app instance
app = create_app()
db = SQLAlchemy()

#region SocketIO Things
@socketio.on("connect")
def handle_connect():
    print("A client connected")

@socketio.on("order_update")
def handle_order_update(data):
    print(f"Order update received: {data}")
    socketio.emit("order_update", data, broadcast=True)
#endregion

#region --- Run the app ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # ✅ Ensure tables exist before running
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)  # ✅ Runs only if executed directly
#endregion