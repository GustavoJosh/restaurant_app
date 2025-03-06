from flask import current_app, render_template, jsonify
from database import db
from models.menu import MenuItem, Recipe
from models.branch import Branch
from models.stock import Ingredient
from flask import flash, redirect, url_for

@current_app.route("/test")
def test_template():
    return render_template("test_waiter.html")   

@current_app.route("/")
def home():
    return render_template("test.html")

@current_app.route("/mobile_dashboard")
def mobile_dashboard():
    return render_template("mobile_dashboard.html")

@current_app.route('/debug/menu')
def debug_menu():
    menu_items = MenuItem.query.all()
    return jsonify([item.name for item in menu_items])

@current_app.route("/Dev")
def dev():
    try:
        # Fetch menu items
        menu_items = db.session.query(MenuItem).filter(MenuItem.is_active == True).all()
        
        # Get all branches
        branches = Branch.query.all()
        
        # Calculate stock for each menu item
        menu_stock = {}
        
        # Track remaining ingredient quantities
        ingredient_usage = {ingredient.id: ingredient.total_quantity for ingredient in db.session.query(Ingredient).all()}
        
        # Calculate the max stock each recipe can produce
        for item in menu_items:
            recipes = Recipe.query.filter_by(menu_item_id=item.id).all()

            if not recipes:
                menu_stock[item.id] = 0
                continue

            min_stock = float('inf')
            for recipe in recipes:
                ingredient = recipe.ingredient
                quantity_used = recipe.quantity_used

                if ingredient.id in ingredient_usage and quantity_used > 0:
                    max_dishes = int(ingredient_usage[ingredient.id] / quantity_used)
                    min_stock = min(min_stock, max_dishes)

            menu_stock[item.id] = max(0, min_stock) if min_stock != float('inf') else 0
        
        return render_template("dev_page.html", menu_items=menu_items, menu_stock=menu_stock, branches=branches)
    except Exception as e:
        flash(f"Error loading dev page: {str(e)}", "danger")
        return redirect(url_for("home"))