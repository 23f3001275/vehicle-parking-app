from flask import render_template,request,redirect,url_for
from create_app import app
from extensions import db
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot

@app.route("/edit_lot/<admin_name>/<login_success>", methods=["GET","POST"])
def editLot(admin_name, login_success):
    # # user=User.query.filter(User.username==user_name).first()
    # user = User.query.filter_by(username=user_name).first_or_404()

    # if request.method == "POST":
    #     user.username = request.form["username"]
    #     user.email = request.form["email"]
    #     user.password = request.form["password"]
    #     user.address = request.form["address"]
    #     user.fullname = request.form["fullname"]
    #     user.pincode = request.form["pincode"]

    #     try:
    #         db.session.commit()
    #         url = url_for('homeUser', user_name=user.username, login_success=login_success)
    #         return redirect(url)
    #         # return redirect("/update/user_name/login_success/")
    #     except:
    #         return "Could not update task"
    # else:
    #     return render_template("User/edit_profile_user.html", admin_name=admin_name, login_success=login_success, user=user)
    pass