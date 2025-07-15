from flask import render_template
from create_app import app

@app.route('/summary_admin<admin_name>/<login_success>')
def summaryAdmin(admin_name,login_success):
    return render_template("Admin/summary_admin.html", admin_name=admin_name, login_success=login_success)