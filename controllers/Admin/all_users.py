from flask import render_template
from create_app import app
from models.user import User

@app.route('/all_users/<admin_name>/<login_success>')
def allUsers(admin_name, login_success):
    users = User.query.all()
    return render_template("Admin/all_users.html", users = users, admin_name=admin_name, login_success=login_success)