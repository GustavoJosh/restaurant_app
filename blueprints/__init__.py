# blueprints/__init__.py
def register_blueprints(app):
    """Register all application blueprints"""
    from blueprints.admin import admin_bp
    from blueprints.api import api_bp
    from blueprints.pos import pos_bp
    from blueprints.stock import stock_bp
    
    
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(pos_bp, url_prefix='/pos')
    app.register_blueprint(stock_bp, url_prefix='/stock')
    

# Explicitly export the function
__all__ = ['register_blueprints']