# blueprints/admin/menu_routes.py
from flask import render_template, request, flash
from models import db
from models.branch import Branch
from blueprints.admin import admin_bp

@admin_bp.route("/branches", methods=["GET", "POST"])
def admin_branches():
    if request.method == "POST":
        try:
            branch_id = request.form["branch_id"]
            action = request.form["action"]

            branch = Branch.query.get(branch_id)
            if branch:
                if action == "open":
                    branch.is_open = True
                elif action == "close":
                    branch.is_open = False
                db.session.commit()
                flash(f"Branch '{branch.name}' updated successfully!", "success")
            else:
                flash("Branch not found", "danger")
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating branch: {str(e)}", "danger")

    branches = Branch.query.all()
    return render_template("admin_branches.html", branches=branches)
