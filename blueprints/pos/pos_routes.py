# blueprints/admin/menu_routes.py
from flask import render_template, request, redirect, url_for, flash
from models.menu import MenuItem
from models.branch import Branch
from models.associations import menu_item_branches
from blueprints.pos import pos_bp

@pos_bp.route("/sell_point")
def sell_point():
    try:
        # Get branch parameter, default to first branch if not provided
        branch_id = request.args.get("branch_id", None)
        if branch_id and branch_id.isdigit():
            branch_id = int(branch_id)
            branch = Branch.query.get(branch_id)
            if not branch:
                flash("Branch not found", "danger")
                branch_id = None
        
        if not branch_id:
            # Get the first branch as default
            first_branch = Branch.query.first()
            if first_branch:
                branch_id = first_branch.id
        
        # Get menu items for this branch
        if branch_id:
            # Query menu items available at this branch
            menu_items = MenuItem.query.join(menu_item_branches).filter(
                menu_item_branches.c.branch_id == branch_id,
                MenuItem.is_active == True
            ).all()
        else:
            # Fallback - show all active menu items
            menu_items = MenuItem.query.filter(MenuItem.is_active == True).all()
            
        # Get all branches for the branch selector
        branches = Branch.query.all()
            
        return render_template("sell_point.html", 
                            menu_items=menu_items, 
                            branches=branches, 
                            current_branch_id=branch_id)
    except Exception as e:
        flash(f"Error loading sell point: {str(e)}", "danger")
        return redirect(url_for("home"))

@pos_bp.route("/waiter_sellpoint")
def waiter_sellpoint():
    try:
        # Get branch parameter
        branch_id = request.args.get("branch_id", None)
        if branch_id and branch_id.isdigit():
            branch_id = int(branch_id)
        else:
            # Get the first branch as default
            first_branch = Branch.query.first()
            if first_branch:
                branch_id = first_branch.id
            
        # Get menu items for this branch
        if branch_id:
            menu_items = MenuItem.query.join(menu_item_branches).filter(
                menu_item_branches.c.branch_id == branch_id,
                MenuItem.is_active == True
            ).all()
        else:
            menu_items = MenuItem.query.filter(MenuItem.is_active == True).all()
            
        # Get all branches for the branch selector
        branches = Branch.query.all()
        
        return render_template("waiter_sellpoint.html", 
                            menu_items=menu_items, 
                            branches=branches,
                            current_branch_id=branch_id)
    except Exception as e:
        flash(f"Error loading waiter sell point: {str(e)}", "danger")
        return redirect(url_for("home"))

