from flask import render_template,request,redirect,url_for, flash
from create_app import app
from models.user import User

@app.route('/login_user',methods=['POST','GET'])
def loginUser():
    if request.method=='POST':
        user_user_name=request.form['user_name']
        user_pass_word=request.form['pass_word']
        user=User.query.filter(User.username==user_user_name,User.password==user_pass_word).first()
        if user:
            flash("You are now logged in","success")
            return redirect(url_for('homeUser',user_name=user.username,login_success=True))
        else:
            flash("User not found","error")
            return render_template('User/login_user.html')
        
    return render_template('User/login_user.html')