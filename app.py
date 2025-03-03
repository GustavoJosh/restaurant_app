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
# Initialize Flask Extensions
db = SQLAlchemy()
socketio = SocketIO()
migrate = Migrate()
cors = CORS()

# Import services and models
from services import update_stock, update_menu_item_stock
from models.menu import MenuItem, Recipe
from models.orders import Order, OrderItem
from models.stock import Ingredient
from models.branch import Branch
from models.associations import menu_item_branches


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
    
    return app

# Create the app instance
app = create_app()

#region Routes
@app.route("/test")
def test_template():
    return render_template("test.html")   

@app.route("/test/waiter")
def test_waiter():
    return render_template("test_waiter.html")   

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/mobile_dashboard")
def mobile_dashboard():
    return render_template("mobile_dashboard.html")

# @app.route("/admin/menu")
# def admin_menu():
#     try:
#         branches = Branch.query.all()  # Fetch all branches

#         # Fetch only active menu items and their branches
#         menu_items = db.session.query(MenuItem).filter(MenuItem.is_active == True).all()

#         # Track remaining ingredient quantities
#         ingredient_usage = {ingredient.id: ingredient.total_quantity for ingredient in db.session.query(Ingredient).all()}

#         # Store dynamically calculated stock for each menu item
#         menu_stock = {}

#         # First pass: calculate the max stock each recipe can produce
#         for item in menu_items:
#             recipes = Recipe.query.filter_by(menu_item_id=item.id).all()

#             if not recipes:
#                 menu_stock[item.id] = 0
#                 continue

#             min_stock = float('inf')
#             for recipe in recipes:
#                 ingredient = recipe.ingredient
#                 quantity_used = recipe.quantity_used

#                 if ingredient.id in ingredient_usage and quantity_used > 0:
#                     max_dishes = int(ingredient_usage[ingredient.id] / quantity_used)
#                     min_stock = min(min_stock, max_dishes)

#             menu_stock[item.id] = max(0, min_stock)

#         # Debugging log (optional)
#         for item in menu_items:
#             print(f"Menu Item: {item.name}, Stock: {menu_stock.get(item.id, 0)}")

#         return render_template("admin_menu.html", menu_items=menu_items, menu_stock=menu_stock, branches=branches)
#     except Exception as e:
#         flash(f"Error loading admin menu: {str(e)}", "danger")
#         return redirect(url_for("home"))

# @app.route("/admin/menu/add", methods=["GET", "POST"])
# def add_menu_item():
#     if request.method == "POST":
#         try:
#             name = request.form["name"]
#             price = float(request.form["price"])
#             branch_ids = request.form.getlist("branch_ids")  # Get multiple selected branches

#             if not branch_ids:
#                 flash("Error: You must select at least one branch!", "danger")
#                 return redirect(url_for("add_menu_item"))

#             new_item = MenuItem(name=name, price=price)
#             db.session.add(new_item)
#             db.session.commit()  # Commit first to get new_item.id

#             # Associate the menu item with selected branches
#             for branch_id in branch_ids:
#                 branch = Branch.query.get(branch_id)
#                 if branch:
#                     new_item.branches.append(branch)

#             db.session.commit()
#             flash("Menu item added successfully!", "success")
#             return redirect(url_for("admin_menu"))
#         except Exception as e:
#             db.session.rollback()
#             flash(f"Error adding menu item: {str(e)}", "danger")
#             return redirect(url_for("add_menu_item"))

#     branches = Branch.query.all()  # Fetch all branches
#     return render_template("add_menu_item.html", branches=branches)

# @app.route("/admin/branches", methods=["GET", "POST"])
# def admin_branches():
#     if request.method == "POST":
#         try:
#             branch_id = request.form["branch_id"]
#             action = request.form["action"]

#             branch = Branch.query.get(branch_id)
#             if branch:
#                 if action == "open":
#                     branch.is_open = True
#                 elif action == "close":
#                     branch.is_open = False
#                 db.session.commit()
#                 flash(f"Branch '{branch.name}' updated successfully!", "success")
#             else:
#                 flash("Branch not found", "danger")
#         except Exception as e:
#             db.session.rollback()
#             flash(f"Error updating branch: {str(e)}", "danger")

#     branches = Branch.query.all()
#     return render_template("admin_branches.html", branches=branches)

# @app.route("/admin/menu/delete/<int:id>", methods=["POST"])
# def delete_menu_item(id):
#     try:
#         item = MenuItem.query.get_or_404(id)

#         # Instead of deleting, perform a soft delete:
#         item.is_active = False
#         db.session.commit()

#         flash("Menu item deactivated successfully!", "success")
#     except Exception as e:
#         db.session.rollback()
#         flash(f"Error deactivating menu item: {str(e)}", "danger")
    
#     return redirect(url_for("admin_menu"))

# @app.route("/admin/menu/edit/<int:id>", methods=["GET", "POST"])
# def edit_menu_item(id):
#     item = MenuItem.query.get_or_404(id)
    
#     if request.method == "POST":
#         try:
#             item.name = request.form["name"]
#             item.price = float(request.form["price"])
            
#             # Clear existing branch associations and add new ones
#             branch_ids = request.form.getlist("branch_ids")
            
#             # Remove all existing branch relationships
#             item.branches = []
            
#             # Add new branch relationships
#             for branch_id in branch_ids:
#                 branch = Branch.query.get(branch_id)
#                 if branch:
#                     item.branches.append(branch)
                    
#             db.session.commit()
#             flash("Menu item updated successfully!", "success")
#             return redirect(url_for("admin_menu"))
#         except Exception as e:
#             db.session.rollback()
#             flash(f"Error updating menu item: {str(e)}", "danger")
#             return redirect(url_for("admin_menu"))
            
#     # Get all branches for the form
#     branches = Branch.query.all()
#     # Get current branch IDs for this menu item
#     current_branch_ids = [branch.id for branch in item.branches]
    
#     return render_template("edit_menu_item.html", item=item, branches=branches, current_branch_ids=current_branch_ids)

# @app.route("/admin/recipes")
# def admin_recipes():
#     recipes = Recipe.query.all()
#     return render_template("admin_recipes.html", recipes=recipes)

# @app.route("/admin/recipes/add", methods=["GET", "POST"])
# def add_recipe():
#     if request.method == "POST":
#         try:
#             menu_item_id = int(request.form["menu_item_id"])
#             ingredient_ids = request.form.getlist("ingredient_id[]")  # Get all ingredient IDs
#             quantities = request.form.getlist("quantity_used[]")  # Get all quantities
#             units = request.form.getlist("unit[]")  # Get all units

#             # Validate input data
#             if not ingredient_ids or not quantities or not units:
#                 flash("Please provide all required recipe information", "danger")
#                 return redirect(url_for("add_recipe"))
                
#             if len(ingredient_ids) != len(quantities) or len(quantities) != len(units):
#                 flash("Mismatch in ingredient data. Please check your inputs.", "danger")
#                 return redirect(url_for("add_recipe"))

#             # Save each ingredient as a separate entry in the Recipe table
#             for i in range(len(ingredient_ids)):
#                 new_recipe = Recipe(
#                     menu_item_id=menu_item_id,
#                     ingredient_id=int(ingredient_ids[i]),
#                     quantity_used=float(quantities[i]),  # Use quantity_used consistently
#                     unit=units[i]  # This now saves in the new unit field
#                 )
#                 db.session.add(new_recipe)
                
#             db.session.commit()
#             # Update stock calculations after all recipes are added
#             for ingredient_id in ingredient_ids:
#                 update_menu_item_stock(int(ingredient_id))
                
#             flash("Recipe added successfully!", "success")
#             return redirect(url_for("admin_menu"))
#         except Exception as e:
#             db.session.rollback()
#             flash(f"Error adding recipe: {str(e)}", "danger")
#             return redirect(url_for("add_recipe"))

#     menu_items = MenuItem.query.all()
#     ingredients = db.session.query(Ingredient).filter_by(is_active=True).all()
#     return render_template("add_recipe.html", menu_items=menu_items, raw_ingredients=ingredients)

# @app.route("/admin/recipes/edit/<int:id>", methods=["GET", "POST"])
# def edit_recipe(id):
#     # Fetch all recipe items linked to the menu item (multiple ingredients)
#     recipe_items = Recipe.query.filter_by(menu_item_id=id).all()

#     if request.method == "POST":
#         try:
#             # Delete existing recipe items (to replace with new ones)
#             Recipe.query.filter_by(menu_item_id=id).delete()

#             # Process new ingredients
#             ingredient_ids = request.form.getlist("ingredient_id[]")
#             quantities = request.form.getlist("quantity_used[]")
#             units = request.form.getlist("unit[]")

#             # Validate inputs
#             if len(ingredient_ids) != len(quantities) or len(quantities) != len(units):
#                 flash("Mismatch in ingredient data. Please check your inputs.", "danger")
#                 return redirect(url_for("edit_recipe", id=id))

#             for i in range(len(ingredient_ids)):
#                 new_recipe = Recipe(
#                     menu_item_id=id,
#                     ingredient_id=int(ingredient_ids[i]),
#                     quantity_used=float(quantities[i]),
#                     unit=units[i]
#                 )
#                 db.session.add(new_recipe)

#             db.session.commit()
#             flash("Recipe updated successfully!", "success")
#             return redirect(url_for("admin_recipes"))
#         except Exception as e:
#             db.session.rollback()
#             flash(f"Error updating recipe: {str(e)}", "danger")
#             return redirect(url_for("edit_recipe", id=id))

#     # Fetch menu item and available ingredients
#     menu_item = MenuItem.query.get_or_404(id)
#     ingredients = Ingredient.query.filter_by(is_active=True).all()

#     return render_template(
#         "edit_recipe.html",
#         menu_item=menu_item,
#         recipe_items=recipe_items,
#         menu_items=MenuItem.query.all(),
#         raw_ingredients=ingredients
#     )

# @app.route("/admin/recipes/delete/<int:id>", methods=["POST"])
# def delete_recipe(id):
#     try:
#         recipe = Recipe.query.get_or_404(id)
#         menu_item_id = recipe.menu_item_id
#         ingredient_id = recipe.ingredient_id
        
#         db.session.delete(recipe)
#         db.session.commit()
        
#         # Update stock after recipe deletion
#         update_menu_item_stock(ingredient_id)
        
#         flash("Recipe deleted successfully!", "success")
#     except Exception as e:
#         db.session.rollback()
#         flash(f"Error deleting recipe: {str(e)}", "danger")
        
#     return redirect(url_for("admin_recipes"))

# def update_menu_item_stock(ingredient_id): 
#     try:
#         ingredient = db.session.get(Ingredient, ingredient_id)
#         if not ingredient:
#             return
            
#         recipes = Recipe.query.filter_by(ingredient_id=ingredient_id).all()
#         for recipe in recipes:
#             menu_item = recipe.menu_item
#             quantity_used = recipe.quantity_used
#             if quantity_used > 0:
#                 max_items = int(ingredient.total_quantity / quantity_used)
#                 menu_item.stock = max_items
#                 db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         print(f"Error updating menu item stock: {str(e)}")

# @app.route("/admin/ingredients/")
# def admin_ingredients():
#     ingredients = db.session.query(Ingredient).filter_by(is_active=True).all()
#     return render_template("admin_ingredients.html", ingredients=ingredients)

# @app.route("/admin/ingredients/add", methods=["GET", "POST"])
# def add_ingredient():
#     if request.method == "POST":
#         try:
#             name = request.form["name"]
#             total_quantity = float(request.form["total_quantity"])
#             unit = request.form["unit"]
            
#             # Validate that the unit is one of the allowed units
#             allowed_units = ["kg", "g", "l", "ml", "piece"]
#             if unit not in allowed_units:
#                 flash(f"Invalid unit. Must be one of: {', '.join(allowed_units)}", "danger")
#                 return redirect(url_for("add_ingredient"))
                
#             new_ingredient = Ingredient(name=name, total_quantity=total_quantity, unit=unit)
#             db.session.add(new_ingredient)
#             db.session.commit()
#             flash("Ingredient added successfully!", "success")
#             return redirect(url_for("admin_ingredients"))
#         except Exception as e:
#             db.session.rollback()
#             flash(f"Error adding ingredient: {str(e)}", "danger")
#             return redirect(url_for("add_ingredient"))
            
#     return render_template("add_ingredient.html")

# @app.route("/admin/ingredients/edit/<int:id>", methods=["GET", "POST"])
# def edit_ingredient(id):
#     ingredient = db.session.get(Ingredient, id) or abort(404)

#     if request.method == "POST":
#         try:
#             ingredient.name = request.form["name"]
#             ingredient.total_quantity = float(request.form["total_quantity"])
#             ingredient.unit = request.form["unit"]
            
#             # Validate unit
#             allowed_units = ["kg", "g", "l", "ml", "piece"]
#             if ingredient.unit not in allowed_units:
#                 flash(f"Invalid unit. Must be one of: {', '.join(allowed_units)}", "danger")
#                 return redirect(url_for("edit_ingredient", id=id))
                
#             db.session.commit()
            
#             # Update any menu items that use this ingredient
#             update_menu_item_stock(id)
            
#             flash("Ingredient updated successfully!", "success")
#             return redirect(url_for("admin_ingredients"))
#         except Exception as e:
#             db.session.rollback()
#             flash(f"Error updating ingredient: {str(e)}", "danger")
#             return redirect(url_for("edit_ingredient", id=id))
            
#     return render_template("edit_ingredient.html", ingredient=ingredient)

# @app.route("/admin/ingredients/delete/<int:id>", methods=["POST"])
# def delete_ingredient(id):
#     try:
#         ingredient = db.session.get(Ingredient, id) or abort(404)

#         # Check if this ingredient is used in any recipes
#         recipes_using_ingredient = Recipe.query.filter_by(ingredient_id=id).count()
#         if recipes_using_ingredient > 0:
#             flash(f"Cannot delete ingredient '{ingredient.name}' because it is used in {recipes_using_ingredient} recipes. Deactivating instead.", "warning")
        
#         # Instead of deleting, mark it as inactive
#         ingredient.is_active = False
#         db.session.commit()
#         flash("Ingredient deactivated successfully!", "success")
#     except Exception as e:
#         db.session.rollback()
#         flash(f"Error deactivating ingredient: {str(e)}", "danger")
    
#     return redirect(url_for("admin_ingredients"))

# @app.route("/admin/orders")
# def admin_orders():
#     return render_template("admin_orders.html")

# @app.route("/sell_point")
# def sell_point():
#     try:
#         # Get branch parameter, default to first branch if not provided
#         branch_id = request.args.get("branch_id", None)
#         if branch_id and branch_id.isdigit():
#             branch_id = int(branch_id)
#             branch = Branch.query.get(branch_id)
#             if not branch:
#                 flash("Branch not found", "danger")
#                 branch_id = None
        
#         if not branch_id:
#             # Get the first branch as default
#             first_branch = Branch.query.first()
#             if first_branch:
#                 branch_id = first_branch.id
        
#         # Get menu items for this branch
#         if branch_id:
#             # Query menu items available at this branch
#             menu_items = MenuItem.query.join(menu_item_branches).filter(
#                 menu_item_branches.c.branch_id == branch_id,
#                 MenuItem.is_active == True
#             ).all()
#         else:
#             # Fallback - show all active menu items
#             menu_items = MenuItem.query.filter(MenuItem.is_active == True).all()
            
#         # Get all branches for the branch selector
#         branches = Branch.query.all()
            
#         return render_template("sell_point.html", 
#                             menu_items=menu_items, 
#                             branches=branches, 
#                             current_branch_id=branch_id)
#     except Exception as e:
#         flash(f"Error loading sell point: {str(e)}", "danger")
#         return redirect(url_for("home"))

# @app.route("/admin/order_history")
# def order_history():
#     try:
#         # Get filters from request
#         status_filter = request.args.get("status", "all")
#         start_date = request.args.get("start_date")
#         end_date = request.args.get("end_date")
#         branch_id = request.args.get("branch_id")

#         # Query all orders
#         query = Order.query

#         # Apply status filter
#         if status_filter and status_filter != "all":
#             query = query.filter(Order.status == status_filter)

#         # Apply branch filter
#         if branch_id and branch_id.isdigit():
#             query = query.filter(Order.branch_id == int(branch_id))

#         # Apply date filter (Convert to datetime)
#         if start_date and end_date:
#             try:
#                 start_date = datetime.strptime(start_date, "%Y-%m-%d")
#                 end_date = datetime.strptime(end_date, "%Y-%m-%d")
#                 # Add one day to end_date to include the entire end date
#                 end_date = datetime.strptime(end_date.strftime("%Y-%m-%d") + " 23:59:59", "%Y-%m-%d %H:%M:%S")
#                 query = query.filter(Order.created_at.between(start_date, end_date))
#             except ValueError:
#                 flash("Invalid date format. Please use YYYY-MM-DD.", "warning")

#         # Get all branches for the branch filter
#         branches = Branch.query.all()
            
#         # Retrieve and order results
#         orders = query.order_by(Order.id.desc()).all()

#         return render_template("admin_order_history.html", 
#                             orders=orders,
#                             branches=branches,
#                             current_filters={
#                                 "status": status_filter,
#                                 "start_date": start_date.strftime("%Y-%m-%d") if start_date else "",
#                                 "end_date": end_date.strftime("%Y-%m-%d") if end_date else "",
#                                 "branch_id": branch_id
#                             })
#     except Exception as e:
#         flash(f"Error loading order history: {str(e)}", "danger")
#         return redirect(url_for("home"))

# @app.route("/waiter_sellpoint")
# def waiter_sellpoint():
#     try:
#         # Get branch parameter
#         branch_id = request.args.get("branch_id", None)
#         if branch_id and branch_id.isdigit():
#             branch_id = int(branch_id)
#         else:
#             # Get the first branch as default
#             first_branch = Branch.query.first()
#             if first_branch:
#                 branch_id = first_branch.id
            
#         # Get menu items for this branch
#         if branch_id:
#             menu_items = MenuItem.query.join(menu_item_branches).filter(
#                 menu_item_branches.c.branch_id == branch_id,
#                 MenuItem.is_active == True
#             ).all()
#         else:
#             menu_items = MenuItem.query.filter(MenuItem.is_active == True).all()
            
#         # Get all branches for the branch selector
#         branches = Branch.query.all()
        
#         return render_template("waiter_sellpoint.html", 
#                             menu_items=menu_items, 
#                             branches=branches,
#                             current_branch_id=branch_id)
#     except Exception as e:
#         flash(f"Error loading waiter sell point: {str(e)}", "danger")
#         return redirect(url_for("home"))


#endregion

#region API
# @app.route("/api/sales_report")
# def sales_report():
#     try:
#         # Get date range parameters (with defaults)
#         start_date = request.args.get("start_date")
#         end_date = request.args.get("end_date")
#         branch_id = request.args.get("branch_id")
        
#         # Build base SQL queries with appropriate filters
#         date_filter = ""
#         branch_filter = ""
        
#         # Process date filters
#         if start_date and end_date:
#             try:
#                 # Validate dates
#                 datetime.strptime(start_date, "%Y-%m-%d")
#                 datetime.strptime(end_date, "%Y-%m-%d")
#                 # Add one day to end_date to include the entire end date
#                 date_filter = f"AND o.created_at BETWEEN '{start_date}' AND '{end_date} 23:59:59'"
#             except ValueError:
#                 # Default to last 30 days if invalid dates
#                 thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
#                 today = datetime.now().strftime("%Y-%m-%d")
#                 date_filter = f"AND o.created_at BETWEEN '{thirty_days_ago}' AND '{today} 23:59:59'"
#         else:
#             # Default to last 30 days if no dates provided
#             thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
#             today = datetime.now().strftime("%Y-%m-%d")
#             date_filter = f"AND o.created_at BETWEEN '{thirty_days_ago}' AND '{today} 23:59:59'"
                
#         # Process branch filter
#         if branch_id and branch_id.isdigit():
#             branch_filter = f"AND o.branch_id = {branch_id}"
        
#         # 1. Daily Sales Query - Using raw SQL for better performance
#         daily_sales_sql = f"""
#         SELECT 
#             DATE(o.created_at) as date,
#             SUM(mi.price * oi.quantity) as revenue
#         FROM 
#             orders o
#         JOIN 
#             order_items oi ON o.id = oi.order_id
#         JOIN 
#             menu_items mi ON oi.menu_item_id = mi.id
#         WHERE 
#             o.status = 'completed'
#             {date_filter}
#             {branch_filter}
#         GROUP BY 
#             DATE(o.created_at)
#         ORDER BY 
#             DATE(o.created_at)
#         """
        
#         daily_sales_results = db.session.execute(text(daily_sales_sql)).fetchall()
#         daily_sales = []
        
#         for row in daily_sales_results:
#             date_str = row[0].strftime("%Y-%m-%d") if hasattr(row[0], 'strftime') else str(row[0])
#             daily_sales.append({
#                 'date': date_str,
#                 'revenue': float(row[1]) if row[1] is not None else 0
#             })
            
#         # If no results, provide sample data
#         if not daily_sales:
#             # Generate last 7 days of sample data
#             today = datetime.now()
#             for i in range(7, 0, -1):
#                 date = today - timedelta(days=i)
#                 daily_sales.append({
#                     'date': date.strftime("%Y-%m-%d"),
#                     'revenue': round(2500 + 1500 * random.random(), 2)  # Random values between 2500-4000
#                 })
        
#         # 2. Peak Hours Query
#         peak_hours_sql = f"""
#         SELECT 
#             EXTRACT(HOUR FROM o.created_at) as hour,
#             COUNT(o.id) as order_count
#         FROM 
#             orders o
#         WHERE 
#             o.status = 'completed'
#             {date_filter}
#             {branch_filter}
#         GROUP BY 
#             EXTRACT(HOUR FROM o.created_at)
#         ORDER BY 
#             EXTRACT(HOUR FROM o.created_at)
#         """
        
#         peak_hours_results = db.session.execute(text(peak_hours_sql)).fetchall()
#         peak_hours = []
        
#         for row in peak_hours_results:
#             peak_hours.append({
#                 'hour': int(row[0]),
#                 'orders': row[1]
#             })
            
#         # Ensure all 24 hours are represented with zeros for missing hours
#         hours_dict = {hour: 0 for hour in range(24)}
#         for hour_data in peak_hours:
#             hours_dict[hour_data['hour']] = hour_data['orders']
            
#         peak_hours = [{'hour': hour, 'orders': count} for hour, count in hours_dict.items()]
        
#         # If no results, provide sample data
#         if sum(h['orders'] for h in peak_hours) == 0:
#             for hour in range(24):
#                 # More orders during lunch and dinner
#                 if 11 <= hour <= 14:  # Lunch
#                     orders = int(15 + 10 * random.random())
#                 elif 17 <= hour <= 21:  # Dinner
#                     orders = int(20 + 15 * random.random())
#                 elif 8 <= hour <= 22:  # Regular hours
#                     orders = int(5 + 5 * random.random())
#                 else:  # Early morning/late night
#                     orders = int(2 * random.random())
                    
#                 peak_hours[hour]['orders'] = orders
        
#         # 3. Best Sellers Query
#         best_sellers_sql = f"""
#         SELECT 
#             mi.id,
#             mi.name,
#             SUM(oi.quantity) as total_sold
#         FROM 
#             menu_items mi
#         JOIN 
#             order_items oi ON mi.id = oi.menu_item_id
#         JOIN 
#             orders o ON oi.order_id = o.id
#         WHERE 
#             o.status = 'completed'
#             {date_filter}
#             {branch_filter}
#         GROUP BY 
#             mi.id, mi.name
#         ORDER BY 
#             SUM(oi.quantity) DESC
#         LIMIT 10
#         """
        
#         best_sellers_results = db.session.execute(text(best_sellers_sql)).fetchall()
#         best_sellers = []
        
#         for row in best_sellers_results:
#             best_sellers.append({
#                 'id': row[0],
#                 'name': row[1],
#                 'sold': row[2]
#             })
            
#         # If no results, provide sample data
#         if not best_sellers:
#             sample_products = [
#                 'Gordita Chicharrón', 
#                 'Gordita Deshebrada', 
#                 'Gordita Queso', 
#                 'Gordita Picadillo', 
#                 'Gordita Frijol',
#                 'Refresco',
#                 'Agua de Jamaica'
#             ]
            
#             for i, name in enumerate(sample_products, 1):
#                 best_sellers.append({
#                     'id': i,
#                     'name': name,
#                     'sold': int(50 + 100 * random.random() * (1 - i/10))  # Higher values for first items
#                 })
        
#         # Return all data
#         return jsonify({
#             'daily_sales': daily_sales,
#             'peak_hours': peak_hours,
#             'best_sellers': best_sellers
#         })
        
#     except Exception as e:
#         print(f"Error generating sales report: {str(e)}")
#         # In case of error, return sample data
#         return jsonify({
#             'error': f"Error generating sales report: {str(e)}",
#             'daily_sales': [
#                 {'date': (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"), 
#                  'revenue': round(2500 + 1500 * random.random(), 2)} 
#                 for i in range(7, 0, -1)
#             ],
#             'peak_hours': [
#                 {'hour': hour, 
#                  'orders': int(20 * random.random()) if 8 <= hour <= 22 else 0} 
#                 for hour in range(24)
#             ],
#             'best_sellers': [
#                 {'id': 1, 'name': 'Gordita Chicharrón', 'sold': int(80 + 40 * random.random())},
#                 {'id': 2, 'name': 'Gordita Deshebrada', 'sold': int(60 + 40 * random.random())},
#                 {'id': 3, 'name': 'Gordita Queso', 'sold': int(50 + 30 * random.random())},
#                 {'id': 4, 'name': 'Refresco', 'sold': int(40 + 30 * random.random())},
#                 {'id': 5, 'name': 'Gordita Picadillo', 'sold': int(30 + 30 * random.random())}
#             ]
#         })
    
# @app.route("/api/order_details/<int:order_id>")
# def order_details(order_id):
#     try:
#         order = Order.query.get_or_404(order_id)
#         order_items = OrderItem.query.filter_by(order_id=order.id).all()

#         items = []
#         for item in order_items:
#             item_details = {
#                 "name": item.menu_item.name,
#                 "quantity": item.quantity,
#                 "price": item.menu_item.price,
#                 "subtotal": item.menu_item.price * item.quantity,
#                 "ingredients": item.selected_ingredients or "Default Recipe"
#             }
#             items.append(item_details)

#         # Get branch info
#         branch = Branch.query.get(order.branch_id)
#         branch_name = branch.name if branch else "Unknown"

#         # Calculate order total
#         order_total = sum(item["subtotal"] for item in items)

#         return jsonify({
#             "order_id": order.id, 
#             "table": order.table_number,
#             "branch": branch_name,
#             "status": order.status,
#             "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
#             "items": items,
#             "total": order_total
#         })
#     except Exception as e:
#         return jsonify({"error": f"Error fetching order details: {str(e)}"}), 500

# @app.route("/api/ingredients/stock")
# def get_ingredient_stock():
#     try:
#         ingredients = db.session.query(Ingredient).filter_by(is_active=True).all()
#         ingredient_data = {
#             "labels": [ingredient.name for ingredient in ingredients],
#             "data": [ingredient.total_quantity for ingredient in ingredients]
#         }
#         return jsonify(ingredient_data)
#     except Exception as e:
#         return jsonify({"error": f"Error fetching stock data: {str(e)}"}), 500
    
# @app.route("/api/order", methods=["POST"])
# def place_order():
#     try:
#         data = request.json
#         print("🔥 Received order data:", data)  # Debugging print
        
#         table_number = data.get("table_number")
#         branch_id = data.get("branch_id")
#         order_items = data.get("items")

#         # Debugging prints to see what is missing
#         print(f"✅ Table Number: {table_number}")
#         print(f"✅ Branch ID: {branch_id}")
#         print(f"✅ Order Items: {order_items}")

#         if not table_number or not branch_id or not order_items:
#             print("❌ Missing required fields!")
#             return jsonify({"error": "Missing table_number, branch_id, or items"}), 400

#         # Validate stock before creating the order
#         insufficient_stock = []
#         for item in order_items:
#             menu_item_id = item["menu_item_id"]
#             quantity = item["quantity"]
            
#             # Get recipes for this menu item
#             recipes = Recipe.query.filter_by(menu_item_id=menu_item_id).all()
            
#             for recipe in recipes:
#                 ingredient = db.session.get(Ingredient, recipe.ingredient_id)
#                 if ingredient:
#                     required_quantity = recipe.quantity_used * quantity
#                     if ingredient.total_quantity < required_quantity:
#                         insufficient_stock.append({
#                             "menu_item": MenuItem.query.get(menu_item_id).name,
#                             "ingredient": ingredient.name,
#                             "available": ingredient.total_quantity,
#                             "required": required_quantity
#                         })
        
#         # If any ingredients have insufficient stock, return error
#         if insufficient_stock:
#             return jsonify({
#                 "error": "Insufficient stock for some items",
#                 "details": insufficient_stock
#             }), 400

#         # If we reach here, stock is sufficient, so create the order
#         new_order = Order(table_number=table_number, status="pending", branch_id=branch_id)
#         db.session.add(new_order)
#         db.session.flush()  # Get the order ID before commit

#         for item in order_items:
#             new_order_item = OrderItem(
#                 order_id=new_order.id,
#                 menu_item_id=item["menu_item_id"],
#                 quantity=item["quantity"]
#             )
#             db.session.add(new_order_item)

#             # ✅ Call the stock update function here!
#             update_stock(new_order_item)

#         db.session.commit()

#         print("✅ Emitting WebSocket event: order_update")  # Debugging print
#         socketio.emit("order_update", {"message": "New order placed!"})

#         return jsonify({"message": "Order placed successfully", "order_id": new_order.id}), 201

#     except Exception as e:
#         db.session.rollback()
#         print(f"🔥 Error processing order: {str(e)}")
#         return jsonify({"error": str(e)}), 500

# @app.route("/api/kitchen/orders", methods=["GET"])
# def kitchen_orders():
#     try:
#         orders = db.session.query(Order).filter(Order.status != "completed").all()
#         order_data = []

#         for order in orders:
#             order_data.append({
#                 "id": order.id,
#                 "table": order.table_number,
#                 "status": order.status,
#                 "items": [
#                     {"name": item.menu_item.name, "quantity": item.quantity}
#                     for item in order.items
#                 ]
#             })

#         return jsonify(order_data)
#     except Exception as e:
#         print(f"Error fetching kitchen orders: {str(e)}")
#         return jsonify({"error": "Error fetching orders", "details": str(e)}), 500

# @app.route("/api/order/complete/<int:order_id>", methods=["POST"])
# def complete_order(order_id):
#     try:
#         order = db.session.get(Order, order_id)
#         if not order:
#             return jsonify({"error": "Order not found"}), 404

#         if order.status == "completed":
#             return jsonify({"message": "Order already completed"}), 400

#         # 🚨 Step 1: Check if we have enough stock
#         insufficient_stock = []
#         for order_item in OrderItem.query.filter_by(order_id=order.id).all():
#             recipes = Recipe.query.filter_by(menu_item_id=order_item.menu_item_id).all()
#             for ingredient_usage in recipes:
#                 ingredient = db.session.get(Ingredient, ingredient_usage.ingredient_id)
#                 if ingredient and ingredient.total_quantity < (ingredient_usage.quantity_used * order_item.quantity):
#                     insufficient_stock.append(f"{ingredient.name} is too low!")

#         # 🚨 Step 2: If stock is too low, reject order completion
#         if insufficient_stock:
#             return jsonify({"error": "Not enough stock!", "details": insufficient_stock}), 400

#         # 🚨 Step 3: Deduct stock if all ingredients are available
#         for order_item in OrderItem.query.filter_by(order_id=order.id).all():
#             for ingredient_usage in Recipe.query.filter_by(menu_item_id=order_item.menu_item_id).all():
#                 ingredient = db.session.get(Ingredient, ingredient_usage.ingredient_id)
#                 if ingredient:
#                     ingredient.total_quantity -= ingredient_usage.quantity_used * order_item.quantity

#         order.status = "completed"
#         db.session.commit()

#         socketio.emit("order_update", {"message": f"Order {order_id} completed!"})
#         return jsonify({"message": "Order completed successfully!"})
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": f"Error completing order: {str(e)}"}), 500
        
# @app.route("/api/order/cancel/<int:order_id>", methods=["POST"])
# def cancel_order(order_id):
#     try:
#         order = db.session.get(Order, order_id)

#         if not order:
#             return jsonify({"error": "Order not found"}), 404

#         if order.status == "completed":
#             return jsonify({"error": "Cannot cancel a completed order"}), 400

#         # 🚀 Delete all associated order items first
#         OrderItem.query.filter_by(order_id=order.id).delete()

#         # Now delete the order itself
#         db.session.delete(order)
#         db.session.commit()

#         # 🔥 Notify Kitchen in Real Time 🔥
#         socketio.emit("order_update", {"message": f"Order {order.id} canceled!"})

#         return jsonify({"message": "Order canceled successfully"}), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500

# @app.route("/api/orders/recent")
# def recent_orders():
#     try:
#         # Get the 5 most recent orders
#         recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
        
#         orders_data = []
#         for order in recent_orders:
#             # Calculate total
#             total = 0
#             for item in order.items:
#                 total += item.quantity * item.menu_item.price
                
#             # Get branch name
#             branch = Branch.query.get(order.branch_id)
#             branch_name = branch.name if branch else "Unknown"
                
#             orders_data.append({
#                 'id': order.id,
#                 'table': order.table_number,
#                 'status': order.status,
#                 'branch': branch_name,
#                 'created_at': order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
#                 'total': total
#             })
            
#         return jsonify(orders_data)
#     except Exception as e:
#         print(f"Error fetching recent orders: {str(e)}")
#         # Return sample data in case of error
#         return jsonify([
#             {
#                 'id': 1025,
#                 'table': 4,
#                 'status': 'completed',
#                 'branch': 'Centro',
#                 'created_at': (datetime.now() - timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S"),
#                 'total': 125.50
#             },
#             {
#                 'id': 1024,
#                 'table': 2,
#                 'status': 'pending',
#                 'branch': 'Centro',
#                 'created_at': (datetime.now() - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"),
#                 'total': 78.25
#             },
#             {
#                 'id': 1023,
#                 'table': 7,
#                 'status': 'completed',
#                 'branch': 'Malecón',
#                 'created_at': (datetime.now() - timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M:%S"),
#                 'total': 210.75
#             }
#         ])
    
# @app.route("/api/dashboard/summary")
# def dashboard_summary():
#     try:
#         # Calculate today's date (with time at 00:00:00)
#         today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
#         tomorrow = today + timedelta(days=1)
        
#         # Get today's orders count
#         orders_today_count = Order.query.filter(
#             Order.created_at >= today,
#             Order.created_at < tomorrow
#         ).count()
        
#         # Calculate total sales today
#         today_sales_result = db.session.query(
#             func.sum(MenuItem.price * OrderItem.quantity)
#         ).join(
#             OrderItem, MenuItem.id == OrderItem.menu_item_id
#         ).join(
#             Order, OrderItem.order_id == Order.id
#         ).filter(
#             Order.created_at >= today,
#             Order.created_at < tomorrow,
#             Order.status == 'completed'
#         ).scalar()
        
#         today_sales = float(today_sales_result) if today_sales_result else 0
        
#         # Get top selling product
#         top_product_result = db.session.query(
#             MenuItem.name,
#             func.sum(OrderItem.quantity).label('total_sold')
#         ).join(
#             OrderItem, MenuItem.id == OrderItem.menu_item_id
#         ).join(
#             Order, OrderItem.order_id == Order.id
#         ).filter(
#             Order.created_at >= today - timedelta(days=7)  # Past week
#         ).group_by(
#             MenuItem.name
#         ).order_by(
#             func.sum(OrderItem.quantity).desc()
#         ).first()
        
#         top_product = top_product_result[0] if top_product_result else "No data"
        
#         # Get inventory alerts (ingredients with low stock)
#         low_stock_threshold = 5  # Items with less than 10 units
#         low_stock_items = Ingredient.query.filter(
#             Ingredient.total_quantity < low_stock_threshold,
#             Ingredient.is_active == True
#         ).count()
        
#         return jsonify({
#             'orders_today': orders_today_count,
#             'sales_today': today_sales,
#             'top_product': top_product,
#             'inventory_alerts': low_stock_items
#         })
#     except Exception as e:
#         print(f"Error generating dashboard summary: {str(e)}")
#         # Return sample data in case of error
#         return jsonify({
#             'orders_today': 36,
#             'sales_today': 2450.75,
#             'top_product': 'Gordita Chicharrón',
#             'inventory_alerts': 2
#         })
        

#endregion

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