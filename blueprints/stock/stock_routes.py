# blueprints/stock/stock_routes.py
from flask import render_template, request, redirect, url_for, flash, jsonify
from models import db
from models.stock import Ingredient
from models.branch import Branch
from models.stock_sale import StockSale
from blueprints.stock import stock_bp
from datetime import datetime, timedelta
from sqlalchemy import func

@stock_bp.route("/dashboard")
def stock_dashboard():
    """Main dashboard for the stock distribution branch"""
    try:
        # Get stock levels
        ingredients = db.session.query(Ingredient).filter_by(is_active=True).all()
        
        # Get all branches except the stock distribution branch (assuming it's branch_id 1)
        # You should adjust this based on your actual branch ID for the stock distributor
        stock_branch_id = 1
        branches = Branch.query.filter(Branch.id != stock_branch_id).all()
        
        return render_template("stock_dashboard.html", 
                               ingredients=ingredients, 
                               branches=branches)
    except Exception as e:
        flash(f"Error loading stock dashboard: {str(e)}", "danger")
        return redirect(url_for("home"))

@stock_bp.route("/sell", methods=["GET", "POST"])
def sell_stock():
    """Interface for creating new stock sales"""
    if request.method == "POST":
        try:
            ingredient_id = int(request.form["ingredient_id"])
            branch_id = int(request.form["branch_id"])
            quantity = float(request.form["quantity"])
            price_per_kg = float(request.form["price_per_kg"])
            notes = request.form.get("notes", "")
            
            ingredient = Ingredient.query.get_or_404(ingredient_id)
            
            # Check if enough stock is available
            if ingredient.total_quantity < quantity:
                flash(f"Not enough {ingredient.name} in stock. Available: {ingredient.total_quantity}{ingredient.unit}", "danger")
                return redirect(url_for("stock.sell_stock"))
            
            # Calculate total price
            total_price = quantity * price_per_kg
            
            # Create new stock sale
            new_sale = StockSale(
                ingredient_id=ingredient_id,
                branch_id=branch_id,
                quantity=quantity,
                price_per_kg=price_per_kg,
                total_price=total_price,
                notes=notes
            )
            
            # Deduct quantity from stock
            ingredient.total_quantity -= quantity
            
            db.session.add(new_sale)
            db.session.commit()
            
            flash(f"Successfully sold {quantity}kg of {ingredient.name} to branch.", "success")
            return redirect(url_for("stock.sale_history"))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Error processing stock sale: {str(e)}", "danger")
            return redirect(url_for("stock.sell_stock"))
    
    # GET request - render form
    ingredients = Ingredient.query.filter_by(is_active=True).all()
    # Get all branches except the stock distribution branch (assuming it's branch_id 1)
    stock_branch_id = 1
    branches = Branch.query.filter(Branch.id != stock_branch_id).all()
    
    return render_template("sell_stock.html", 
                          ingredients=ingredients, 
                          branches=branches)

@stock_bp.route("/history")
def sale_history():
    """View history of stock sales"""
    try:
        # Get filters from request
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        branch_id = request.args.get("branch_id")
        ingredient_id = request.args.get("ingredient_id")
        
        # Base query
        query = StockSale.query.join(Ingredient).join(Branch)
        
        # Apply filters
        if branch_id and branch_id.isdigit():
            query = query.filter(StockSale.branch_id == int(branch_id))
            
        if ingredient_id and ingredient_id.isdigit():
            query = query.filter(StockSale.ingredient_id == int(ingredient_id))
            
        # Apply date filter
        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                # Add a day to end_date to make it inclusive
                end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
                query = query.filter(StockSale.created_at.between(start, end))
            except ValueError:
                flash("Invalid date format. Please use YYYY-MM-DD.", "warning")
        
        # Execute query with sorting
        sales = query.order_by(StockSale.created_at.desc()).all()
        
        # Get all branches and ingredients for filter dropdowns
        branches = Branch.query.all()
        ingredients = Ingredient.query.filter_by(is_active=True).all()
        
        return render_template("stock_history.html", 
                              sales=sales,
                              branches=branches,
                              ingredients=ingredients,
                              current_filters={
                                  "start_date": start_date,
                                  "end_date": end_date,
                                  "branch_id": branch_id,
                                  "ingredient_id": ingredient_id
                              })
    except Exception as e:
        flash(f"Error loading sales history: {str(e)}", "danger")
        return redirect(url_for("stock.stock_dashboard"))