from flask import render_template,request,redirect,url_for, flash
from create_app import app
from extensions import db
from models.admin import Admin
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot

@app.route("/add_lot_admin/<admin_name>/<login_success>", methods=["POST","GET"])
def addLotAdmin(admin_name, login_success):
    admin = Admin.query.filter_by(username=admin_name).first_or_404()

    if request.method == 'POST':
        lot_loc_name = request.form['location_name']
        lot_price = request.form['price']
        lot_address = request.form['address']
        lot_pincode = request.form['pincode']
        lot_max_spots = request.form['max_spots']

        new_lot = ParkingLot(prime_loc_name = lot_loc_name, 
                             price = lot_price, 
                             address = lot_address, 
                             pincode = lot_pincode, 
                             max_spots = lot_max_spots,
                             admin_id=admin.id)
        
        try:
            db.session.add(new_lot)
            db.session.commit()

            for i in range(new_lot.max_spots):
                new_spot = ParkingSpot(lot_id=new_lot.id)
                db.session.add(new_spot)
            db.session.commit()

            flash("Lot is added","success")
            url = url_for('homeAdmin', admin_name=admin_name, login_success=login_success)
            return redirect(url)
        except:
            flash("Could not add lot","error")
            return render_template('Admin/add_lot.html')
        
    return render_template("Admin/add_lot.html", admin_name=admin_name, login_success=login_success)