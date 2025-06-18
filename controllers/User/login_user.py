from flask import render_template,request,redirect,url_for
from create_app import app
from extensions import db
from models.user import User

@app.route('/login',methods=['POST','GET'])
def login_user():
    if request.method=='POST':
        user_user_name=request.form['user_name']
        user_pass_word=request.form['pass_word']
        print(f"Trying to login: {user_user_name}")

        user=User.query.filter(User.username==user_user_name,User.password==user_pass_word).first()

        if user:
            url = url_for('home_user', user_name=user.username, login_success=True)
            return redirect(url)
        else:
            return "User not found"

    return render_template('User/login_user.html')