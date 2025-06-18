from flask import Flask,render_template,request,redirect,url_for,session
from create_app import app
from extensions import db
from models import User
from controllers.User import *

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db.init_app(app)

# @app.route('/')
# def landingPage():
#     return "This is the landing page"

# @app.route('/login')
# def loginUser():
#     return render_template("User/login_user.html")

@app.route('/home_user/<user_name>/<login_success>')
def home_user(user_name,login_success):
    return render_template("User/home_user.html", user_name=user_name, login_success=login_success)

# @app.route('/register')
# def registerUser():
#     return render_template("User/register_user.html")

@app.route('/summary')
def summaryUser():
    return render_template("User/summary_user.html")

@app.route('/search_parking/<user_name>/<login_success>')
def search_parking(user_name,login_success):
    return render_template("User/search_parking_user.html", user_name=user_name, login_success=login_success)

@app.route('/all_users')
def registerUser():
    users = User.query.all()
    return render_template("Admin/all_users.html", users = users)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)