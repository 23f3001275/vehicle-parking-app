from flask import render_template, request
from create_app import app
from models.parking_lot import ParkingLot

@app.route('/search_parking/<user_name>/<login_success>', methods=['POST','GET'])
def searchParking(user_name,login_success):
    lot_data=None
    lots = ParkingLot.query.all()
    if request.method == 'POST':
        search_name = request.form['loc_name']
        if search_name:
            lot_data = ParkingLot.query.filter(ParkingLot.prime_loc_name.ilike(f"%{search_name}%")).all()


    return render_template("User/search_parking_user.html", user_name=user_name, login_success=login_success, lots=lots, lot_data=lot_data)