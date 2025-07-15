from flask import render_template,request,redirect,url_for, flash
from create_app import app
from models.user import User

@app.route('/login_user',methods=['POST','GET'])
def loginUser():
    if request.method=='POST':
        user_user_name=request.form['user_name']
        user_pass_word=request.form['pass_word']
        print(f"Trying to login: {user_user_name}")

        user=User.query.filter(User.username==user_user_name,User.password==user_pass_word).first()

        if user:
            url = url_for('homeUser', user_name=user.username, login_success=True)
            return redirect(url)
        else:
            return render_template('User/login_user.html', login_success1=True)

    return render_template('User/login_user.html', login_success1=False)