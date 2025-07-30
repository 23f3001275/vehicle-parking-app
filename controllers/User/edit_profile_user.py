from flask import render_template,request,redirect,url_for,flash
from create_app import app
from extensions import db
from models.user import User

@app.route('/edit_profile_user/<user_name>/<login_success>',methods=['POST','GET'])
def editProfileUser(user_name,login_success):    
    user=User.query.filter(User.username==user_name).first()
    if request.method=='POST':
        user.email=request.form['email']
        user.username =request.form['username']
        user.password=request.form['password']
        user.fullname=request.form['fullname']
        user.address=request.form['address']
        user.pincode=request.form['pincode']

        try:
            db.session.commit()
            flash("Updated successfully","success")
            return redirect(url_for('homeUser',user_name=user.username,login_success=True))
        except:
            flash("There was problem editing your profile","error") 
            return render_template('User/edit_profile_user.html',user=user,login_success=login_success,user_name=user_name)
        
    return render_template('User/edit_profile_user.html',user=user,login_success=login_success,user_name=user_name)