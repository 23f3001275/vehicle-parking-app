from flask import render_template
from create_app import app
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.reserved_parking_spot import ReservedParkingSpot
from models.user import User

@app.route('/home_user/<user_name>/<login_success>')
def homeUser(user_name,login_success):
    user=User.query.filter(User.username==user_name).first()
    reservations=ReservedParkingSpot.query.filter(ReservedParkingSpot.user_id==user.id).all()
    all_user_data=[]
    for reservation in reservations:
        spot=ParkingSpot.query.filter(ParkingSpot.reserved_spot==reservation.spot_id).all()
        lot=ParkingLot.query.filter(ParkingLot.spot_in_lot==spot.lot_id).all()
            
        all_user_data=[{
            'prime_loc_name':lot.prime_loc_name,
            'lot_id':lot.id,
            'price': lot.price,
            'park_timestamp':reservation.park_timestamp,
            'leaving_timestamp':reservation.leaving_timestamp
        }]
    return render_template("User/home_user.html", user_name=user_name, login_success=login_success,all_user_data=all_user_data)