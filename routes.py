from flask import current_app, render_template


@current_app.route("/test")
def test_template():
    return render_template("test.html")   

@current_app.route("/test/waiter")
def test_waiter():
    return render_template("test_waiter.html")   

@current_app.route("/")
def home():
    return render_template("index.html")

@current_app.route("/mobile_dashboard")
def mobile_dashboard():
    return render_template("mobile_dashboard.html")