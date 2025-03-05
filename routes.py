from flask import current_app, render_template

@current_app.route("/test")
def test_template():
    return render_template("test_waiter.html")   

@current_app.route("/")
def home():
    return render_template("test.html")

@current_app.route("/mobile_dashboard")
def mobile_dashboard():
    return render_template("mobile_dashboard.html")

@current_app.route("/Dev")
def dev():
    return render_template("dev_page.html")