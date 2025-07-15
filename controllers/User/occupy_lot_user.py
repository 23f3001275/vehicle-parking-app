from flask import render_template,request,redirect,url_for
from create_app import app
from extensions import db
from models.user import User
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.reserved_parking_spot import ReservedParkingSpot
from datetime import datetime

@app.route('/occupy_lot_user/<user_name>/<login_success>/<lot_id>/<spot_id>',methods=['POST','GET'])
def occupyLotUser(user_name, login_success,lot_id,spot_id):
    user=User.query.filter(User.username==user_name).first()
    lot=ParkingLot.query.filter(ParkingLot.id==lot_id).first()
    spot=ParkingSpot.query.filter(ParkingSpot.lot_id==lot_id,ParkingSpot.status=="R",ParkingSpot.id==spot_id).first()
    if request.method=='POST':
        vehicle_no=request.form['vehicle_no']
        park_timestamp_str=request.form['park_timestamp']
        park_timestamp = datetime.strptime(park_timestamp_str, '%Y-%m-%dT%H:%M')
        lt=request.form['leave_timestamp']
        if not lt:
            leave_timestamp=None
        else:
            leave_timestamp=lt
        
        spot.status="R"

        reservation=ReservedParkingSpot(spot_id=spot.id,
                                        user_id=user.id,
                                        reserve_timestamp=datetime.now(),
                                        reserved_status=True,
                                        vehicle_no=vehicle_no,
                                        park_timestamp=park_timestamp,
                                        leave_timestamp=leave_timestamp)
        
                 
        try:
            db.session.add(reservation)
            db.session.commit()
            return redirect(url_for('home_user',user_name=user_name,login_success=login_success))
        except:
            pass
    
    return render_template('User/home_user.html',user_name=user_name, login_success=login_success,lot=lot,user=user,spot=spot) 