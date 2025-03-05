# blueprints/admin/menu_routes.py
from flask import render_template, request, redirect, url_for, flash
from models import db
from models.menu import MenuItem
from models.branch import Branch
from models.menu import Recipe  # Add this missing import
from models.stock import Ingredient  # Add this missing import
from blueprints.admin import admin_bp


@admin_bp.route("/menu")
def admin_menu():
    try:
        branches = Branch.query.all()  # Fetch all branches

        # Fetch only active menu items and their branches
        menu_items = db.session.query(MenuItem).filter(MenuItem.is_active == True).all()

        # Track remaining ingredient quantities
        ingredient_usage = {ingredient.id: ingredient.total_quantity for ingredient in db.session.query(Ingredient).all()}

        # Store dynamically calculated stock for each menu item
        menu_stock = {}

        # First pass: calculate the max stock each recipe can produce
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

            menu_stock[item.id] = max(0, min_stock)

        # Debugging log (optional)
        for item in menu_items:
            print(f"Menu Item: {item.name}, Stock: {menu_stock.get(item.id, 0)}")

        return render_template("admin_menu.html", menu_items=menu_items, menu_stock=menu_stock, branches=branches)
    except Exception as e:
        flash(f"Error loading admin menu: {str(e)}", "danger")
        return redirect(url_for("home"))

@admin_bp.route("/menu/add", methods=["GET", "POST"])
def add_menu_item():
    if request.method == "POST":
        try:
            name = request.form["name"]
            price = float(request.form["price"])
            branch_ids = request.form.getlist("branch_ids")  # Get multiple selected branches

            if not branch_ids:
                flash("Error: You must select at least one branch!", "danger")
                return redirect(url_for("admin.add_menu_item"))

            new_item = MenuItem(name=name, price=price)
            db.session.add(new_item)
            db.session.commit()  # Commit first to get new_item.id

            # Associate the menu item with selected branches
            for branch_id in branch_ids:
                branch = Branch.query.get(branch_id)
                if branch:
                    new_item.branches.append(branch)

            db.session.commit()
            flash("Menu item added successfully!", "success")
            return redirect(url_for("admin.admin_menu"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding menu item: {str(e)}", "danger")
            return redirect(url_for("admin.add_menu_item"))

    branches = Branch.query.all()  # Fetch all branches
    return render_template("add_menu_item.html", branches=branches)

@admin_bp.route("/menu/delete/<int:id>", methods=["POST"])
def delete_menu_item(id):
    try:
        item = MenuItem.query.get_or_404(id)

        # Instead of deleting, perform a soft delete:
        item.is_active = False
        db.session.commit()

        flash("Menu item deactivated successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deactivating menu item: {str(e)}", "danger")
    
    return redirect(url_for("admin.admin_menu"))

@admin_bp.route("/menu/edit/<int:id>", methods=["GET", "POST"])
def edit_menu_item(id):
    item = MenuItem.query.get_or_404(id)
    
    if request.method == "POST":
        try:
            item.name = request.form["name"]
            item.price = float(request.form["price"])
            
            # Clear existing branch associations and add new ones
            branch_ids = request.form.getlist("branch_ids")
            
            # Remove all existing branch relationships
            item.branches = []
            
            # Add new branch relationships
            for branch_id in branch_ids:
                branch = Branch.query.get(branch_id)
                if branch:
                    item.branches.append(branch)
                    
            db.session.commit()
            flash("Menu item updated successfully!", "success")
            return redirect(url_for("admin.admin_menu"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating menu item: {str(e)}", "danger")
            return redirect(url_for("admin.admin_menu"))
            
    # Get all branches for the form
    branches = Branch.query.all()
    # Get current branch IDs for this menu item
    current_branch_ids = [branch.id for branch in item.branches]
    
    return render_template("edit_menu_item.html", item=item, branches=branches, current_branch_ids=current_branch_ids)
