# blueprints/admin/menu_routes.py
from flask import render_template, request, redirect, url_for, flash
from models.branch import Branch
from blueprints.admin import admin_bp
from models import db
from models.orders import Order
import datetime

@admin_bp.route("/orders")
def admin_orders():
    return render_template("admin_orders.html")

@admin_bp.route("/order_history")
def order_history():
    try:
        # Get filters from request
        status_filter = request.args.get("status", "all")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        branch_id = request.args.get("branch_id")

        # Query all orders
        query = Order.query

        # Apply status filter
        if status_filter and status_filter != "all":
            query = query.filter(Order.status == status_filter)

        # Apply branch filter
        if branch_id and branch_id.isdigit():
            query = query.filter(Order.branch_id == int(branch_id))

        # Apply date filter (Convert to datetime)
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
                # Add one day to end_date to include the entire end date
                end_date = datetime.strptime(end_date.strftime("%Y-%m-%d") + " 23:59:59", "%Y-%m-%d %H:%M:%S")
                query = query.filter(Order.created_at.between(start_date, end_date))
            except ValueError:
                flash("Invalid date format. Please use YYYY-MM-DD.", "warning")

        # Get all branches for the branch filter
        branches = Branch.query.all()
            
        # Retrieve and order results
        orders = query.order_by(Order.id.desc()).all()

        return render_template("admin_order_history.html", 
                            orders=orders,
                            branches=branches,
                            current_filters={
                                "status": status_filter,
                                "start_date": start_date.strftime("%Y-%m-%d") if start_date else "",
                                "end_date": end_date.strftime("%Y-%m-%d") if end_date else "",
                                "branch_id": branch_id
                            })
    except Exception as e:
        flash(f"Error loading order history: {str(e)}", "danger")
        return redirect(url_for("home"))
