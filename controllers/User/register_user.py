from flask import render_template, redirect, request
from create_app import app
from extensions import db
from models.user import User 

@app.route("/register", methods=["POST","GET"])
def register_user():
    if request.method == 'POST':
        user_email = request.form['email']
        user_username = request.form['username']
        user_password = request.form['password']
        user_fullname = request.form['fullname']
        user_address = request.form['address']
        user_pincode = request.form['pincode']

        new_user = User(email = user_email, 
                        username = user_username, 
                        password = user_password, 
                        fullname = user_fullname, 
                        address = user_address, 
                        pincode = user_pincode)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
        except:
            return "There was a problem registering you"
        
    return render_template("User/register_user.html")