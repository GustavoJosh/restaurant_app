# blueprints/admin/menu_routes.py
from flask import render_template, request, redirect, url_for, flash
from models import db
from models.menu import MenuItem
from models.menu import Recipe  # Add this missing import
from models.stock import Ingredient  # Add this missing import
from services import update_menu_item_stock 
from blueprints.admin import admin_bp


@admin_bp.route("/recipes")
def admin_recipes():
    recipes = Recipe.query.all()
    return render_template("admin.admin_recipes.html", recipes=recipes)

@admin_bp.route("/recipes/add", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        try:
            menu_item_id = int(request.form["menu_item_id"])
            ingredient_ids = request.form.getlist("ingredient_id[]")  # Get all ingredient IDs
            quantities = request.form.getlist("quantity_used[]")  # Get all quantities
            units = request.form.getlist("unit[]")  # Get all units

            # Validate input data
            if not ingredient_ids or not quantities or not units:
                flash("Please provide all required recipe information", "danger")
                return redirect(url_for("admin.add_recipe"))
                
            if len(ingredient_ids) != len(quantities) or len(quantities) != len(units):
                flash("Mismatch in ingredient data. Please check your inputs.", "danger")
                return redirect(url_for("admin.add_recipe"))

            # Save each ingredient as a separate entry in the Recipe table
            for i in range(len(ingredient_ids)):
                new_recipe = Recipe(
                    menu_item_id=menu_item_id,
                    ingredient_id=int(ingredient_ids[i]),
                    quantity_used=float(quantities[i]),  # Use quantity_used consistently
                    unit=units[i]  # This now saves in the new unit field
                )
                db.session.add(new_recipe)
                
            db.session.commit()
            # Update stock calculations after all recipes are added
            for ingredient_id in ingredient_ids:
                update_menu_item_stock(int(ingredient_id))
                
            flash("Recipe added successfully!", "success")
            return redirect(url_for("admin.admin_menu"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding recipe: {str(e)}", "danger")
            return redirect(url_for("admin.add_recipe"))

    menu_items = MenuItem.query.all()
    ingredients = db.session.query(Ingredient).filter_by(is_active=True).all()
    return render_template("admin.add_recipe.html", menu_items=menu_items, raw_ingredients=ingredients)

@admin_bp.route("/recipes/edit/<int:id>", methods=["GET", "POST"])
def edit_recipe(id):
    # Fetch all recipe items linked to the menu item (multiple ingredients)
    recipe_items = Recipe.query.filter_by(menu_item_id=id).all()

    if request.method == "POST":
        try:
            # Delete existing recipe items (to replace with new ones)
            Recipe.query.filter_by(menu_item_id=id).delete()

            # Process new ingredients
            ingredient_ids = request.form.getlist("ingredient_id[]")
            quantities = request.form.getlist("quantity_used[]")
            units = request.form.getlist("unit[]")

            # Validate inputs
            if len(ingredient_ids) != len(quantities) or len(quantities) != len(units):
                flash("Mismatch in ingredient data. Please check your inputs.", "danger")
                return redirect(url_for("admin.edit_recipe", id=id))

            for i in range(len(ingredient_ids)):
                new_recipe = Recipe(
                    menu_item_id=id,
                    ingredient_id=int(ingredient_ids[i]),
                    quantity_used=float(quantities[i]),
                    unit=units[i]
                )
                db.session.add(new_recipe)

            db.session.commit()
            flash("Recipe updated successfully!", "success")
            return redirect(url_for("admin.admin_recipes"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating recipe: {str(e)}", "danger")
            return redirect(url_for("admin.edit_recipe", id=id))

    # Fetch menu item and available ingredients
    menu_item = MenuItem.query.get_or_404(id)
    ingredients = Ingredient.query.filter_by(is_active=True).all()

    return render_template(
        "edit_recipe.html",
        menu_item=menu_item,
        recipe_items=recipe_items,
        menu_items=MenuItem.query.all(),
        raw_ingredients=ingredients
    )

@admin_bp.route("/recipes/delete/<int:id>", methods=["POST"])
def delete_recipe(id):
    try:
        recipe = Recipe.query.get_or_404(id)
        menu_item_id = recipe.menu_item_id
        ingredient_id = recipe.ingredient_id
        
        db.session.delete(recipe)
        db.session.commit()
        
        # Update stock after recipe deletion
        update_menu_item_stock(ingredient_id)
        
        flash("Recipe deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting recipe: {str(e)}", "danger")
        
    return redirect(url_for("admin.admin_recipes"))
