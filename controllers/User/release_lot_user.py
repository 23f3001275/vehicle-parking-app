from flask import render_template,request,redirect,url_for,flash
from create_app import app
from extensions import db
from models.user import User
from models.parking_spot import ParkingSpot
from models.parking_lot import ParkingLot
from models.reserved_parking_spot import ReservedParkingSpot
from datetime import datetime
import math
@app.route('/release_lot_user/<user_name>/<login_success>/<lot_id>/<spot_id>',methods=["POST","GET"])
def releaseLotUser(user_name, login_success,lot_id,spot_id):
    spot_id = int(spot_id)
    lot_id = int(lot_id)
    user=User.query.filter(User.username==user_name).first()
    reservation=ReservedParkingSpot.query.filter(ReservedParkingSpot.user_id==user.id,ReservedParkingSpot.reserve_status==1,ReservedParkingSpot.spot_id==spot_id).first()
    lot=ParkingLot.query.filter(ParkingLot.id==lot_id).first()
    spot=ParkingSpot.query.filter(ParkingSpot.id==spot_id,ParkingSpot.status=="O").first()
    if request.method=="POST":
        reservation.leave_timestamp=datetime.now()
        
        dt1 = reservation.park_timestamp
        dt2 = datetime.now()
        
        diff = dt2 - dt1
        hours = diff.total_seconds() / 3600
        total_hours=math.ceil(hours)
        price=((total_hours)*(lot.price))
        reservation.park_cost_per_unit_time=price
        spot.status="A"
        reservation.reserve_status=False
        
        try:
            db.session.commit()
            flash("Spot has been released","success")
            return redirect(url_for('homeUser',user_name=user_name, login_success=login_success))
        except:
            flash("Spot could not be released","error")
            return redirect(url_for('homeUser',user_name=user_name, login_success=login_success))
        
    return render_template('User/home_user.html',user_name=user_name, login_success=login_success) 