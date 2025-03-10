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

@admin_bp.route("/menu/modifications/<int:id>", methods=["GET", "POST"])
def edit_menu_item_modifications(id):
    """Edit the standard modifications for a menu item"""
    try:
        item = MenuItem.query.get_or_404(id)
        
        if request.method == "POST":
            try:
                # Parse the modification data from the form
                modifications = {
                    "additions": [],
                    "removals": [],
                    "substitutions": []
                }
                
                # Process additions
                addition_ids = request.form.getlist("addition_ingredient_id[]")
                addition_names = request.form.getlist("addition_name[]")
                addition_prices = request.form.getlist("addition_price[]")
                
                for i in range(len(addition_ids)):
                    if i < len(addition_names) and i < len(addition_prices) and addition_ids[i]:
                        modifications["additions"].append({
                            "ingredient_id": int(addition_ids[i]),
                            "name": addition_names[i],
                            "price": float(addition_prices[i]),
                            "quantity": 1.0  # Default quantity
                        })
                
                # Process removals
                removal_ids = request.form.getlist("removal_ingredient_id[]")
                removal_names = request.form.getlist("removal_name[]")
                
                for i in range(len(removal_ids)):
                    if i < len(removal_names) and removal_ids[i]:
                        modifications["removals"].append({
                            "ingredient_id": int(removal_ids[i]),
                            "name": removal_names[i],
                            "price": 0.0  # Removals are typically free
                        })
                
                # Process substitutions
                sub_original_ids = request.form.getlist("sub_original_id[]")
                sub_replacement_ids = request.form.getlist("sub_replacement_id[]")
                sub_names = request.form.getlist("sub_name[]")
                sub_prices = request.form.getlist("sub_price[]")
                
                for i in range(len(sub_original_ids)):
                    if (i < len(sub_replacement_ids) and 
                        i < len(sub_names) and 
                        i < len(sub_prices) and
                        sub_original_ids[i] and
                        sub_replacement_ids[i]):
                        modifications["substitutions"].append({
                            "ingredient_id": int(sub_original_ids[i]),
                            "replacement_id": int(sub_replacement_ids[i]),
                            "name": sub_names[i],
                            "price": float(sub_prices[i])
                        })
                
                # Update the menu item with the new modifications
                item.standard_modifications = modifications
                db.session.commit()
                
                flash("Menu item modifications updated successfully!", "success")
                return redirect(url_for("admin.admin_menu"))
            except Exception as e:
                db.session.rollback()
                flash(f"Error updating modifications: {str(e)}", "danger")
                return redirect(url_for("admin.edit_menu_item_modifications", id=id))
        
        # For GET requests, prepare the form
        current_mods = item.standard_modifications or {
            "additions": [],
            "removals": [],
            "substitutions": []
        }
        
        # Get all ingredients for dropdowns
        ingredients = Ingredient.query.filter_by(is_active=True).all()
        
        # Get ingredients used in this item's recipes
        recipe_ingredients = []
        for recipe in Recipe.query.filter_by(menu_item_id=item.id).all():
            ingredient = Ingredient.query.get(recipe.ingredient_id)
            if ingredient:
                recipe_ingredients.append({
                    "id": ingredient.id,
                    "name": ingredient.name,
                    "quantity": recipe.quantity_used,
                    "unit": recipe.unit
                })
        
        return render_template(
            "edit_menu_item_modifications.html",
            item=item,
            modifications=current_mods,
            ingredients=ingredients,
            recipe_ingredients=recipe_ingredients
        )
    except Exception as e:
        flash(f"Error loading modifications page: {str(e)}", "danger")
        return redirect(url_for("admin.admin_menu"))