from flask import render_template,request,redirect,url_for
from create_app import app
from models.admin import Admin

@app.route('/login_admin',methods=['POST','GET'])
def loginAdmin():
    if request.method=='POST':
        admin_user_name=request.form['user_name']
        admin_pass_word=request.form['pass_word']
        print(f"Trying to login: {admin_user_name}")

        admin=Admin.query.filter(Admin.username==admin_user_name,Admin.password==admin_pass_word).first()

        if admin:
            url = url_for('homeAdmin', admin_name=admin.username, login_success=True)
            return redirect(url)
        else:
            return render_template('Admin/login_admin.html', login_success1=True)

    return render_template('Admin/login_admin.html', login_success1=False)