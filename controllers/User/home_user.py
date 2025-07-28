from flask import render_template,flash
from create_app import app
from extensions import db
from models.user import User
from models.parking_spot import ParkingSpot
from models.parking_lot import ParkingLot
from models.reserved_parking_spot import ReservedParkingSpot
from datetime import datetime

@app.route('/home_user/<user_name>/<login_success>')
def homeUser(user_name,login_success):
    user=User.query.filter(User.username==user_name).first()
    reservations=ReservedParkingSpot.query.filter(ReservedParkingSpot.user_id==user.id).all()
    all_user_data=[]
    user_history=[]
    for reservation in reservations:
        spots=ParkingSpot.query.filter(ParkingSpot.id==reservation.spot_id).all()
        for spot in spots:
            lots=ParkingLot.query.filter(ParkingLot.id==spot.lot_id).all()
            for lot in lots:
                all_user_data.append({
                    'prime_loc_name':lot.prime_loc_name,
                    'lot_id':lot.id,
                    'price': lot.price,
                    'park_timestamp':reservation.park_timestamp,
                    'leave_timestamp':reservation.leave_timestamp,
                    'status':str(spot.status),
                    'spot_id':spot.id,
                    'reserve_status':reservation.reserve_status,
                    'vehicle_no':reservation.vehicle_no,
                    'reserve_timestamp':reservation.reserve_timestamp,
                    'cost':reservation.park_cost_per_unit_time
                    
                })
        if reservation.reserve_status and datetime.now()>reservation.park_timestamp:
            spot.status="O"
                
    try:
        db.session.commit()
    except:
        pass
                
    return render_template('user/home_user.html',user_name=user_name, login_success=login_success,all_user_data=all_user_data,user_history=user_history) 