# blueprints/admin/menu_routes.py
from flask import render_template, request, redirect, url_for, flash, abort
from models import db
from models.menu import Recipe  # Add this missing import
from models.stock import Ingredient  # Add this missing import
from blueprints.admin import admin_bp
from services import update_menu_item_stock

@admin_bp.route("/ingredients/")
def admin_ingredients():
    ingredients = db.session.query(Ingredient).filter_by(is_active=True).all()
    return render_template("admin_ingredients.html", ingredients=ingredients)

@admin_bp.route("/ingredients/add", methods=["GET", "POST"])
def add_ingredient():
    if request.method == "POST":
        try:
            name = request.form["name"]
            total_quantity = float(request.form["total_quantity"])
            unit = request.form["unit"]
            
            # Validate that the unit is one of the allowed units
            allowed_units = ["kg", "g", "l", "ml", "piece"]
            if unit not in allowed_units:
                flash(f"Invalid unit. Must be one of: {', '.join(allowed_units)}", "danger")
                return redirect(url_for("admin.add_ingredient"))
                
            new_ingredient = Ingredient(name=name, total_quantity=total_quantity, unit=unit)
            db.session.add(new_ingredient)
            db.session.commit()
            flash("Ingredient added successfully!", "success")
            return redirect(url_for("admin.admin_ingredients"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding ingredient: {str(e)}", "danger")
            return redirect(url_for("admin.add_ingredient"))
            
    return render_template("add_ingredient.html")

@admin_bp.route("/ingredients/edit/<int:id>", methods=["GET", "POST"])
def edit_ingredient(id):
    ingredient = db.session.get(Ingredient, id) or abort(404)

    if request.method == "POST":
        try:
            ingredient.name = request.form["name"]
            ingredient.total_quantity = float(request.form["total_quantity"])
            ingredient.unit = request.form["unit"]
            
            # Validate unit
            allowed_units = ["kg", "g", "l", "ml", "piece"]
            if ingredient.unit not in allowed_units:
                flash(f"Invalid unit. Must be one of: {', '.join(allowed_units)}", "danger")
                return redirect(url_for("admin.edit_ingredient", id=id))
                
            db.session.commit()
            
            # Update any menu items that use this ingredient
            update_menu_item_stock(id)
            
            flash("Ingredient updated successfully!", "success")
            return redirect(url_for("admin.admin_ingredients"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating ingredient: {str(e)}", "danger")
            return redirect(url_for("admin.edit_ingredient", id=id))
            
    return render_template("edit_ingredient.html", ingredient=ingredient)

@admin_bp.route("/ingredients/delete/<int:id>", methods=["POST"])
def delete_ingredient(id):
    try:
        ingredient = db.session.get(Ingredient, id) or abort(404)

        # Check if this ingredient is used in any recipes
        recipes_using_ingredient = Recipe.query.filter_by(ingredient_id=id).count()
        if recipes_using_ingredient > 0:
            flash(f"Cannot delete ingredient '{ingredient.name}' because it is used in {recipes_using_ingredient} recipes. Deactivating instead.", "warning")
        
        # Instead of deleting, mark it as inactive
        ingredient.is_active = False
        db.session.commit()
        flash("Ingredient deactivated successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deactivating ingredient: {str(e)}", "danger")
    
    return redirect(url_for("admin.admin_ingredients"))
