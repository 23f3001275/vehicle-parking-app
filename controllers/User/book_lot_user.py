from flask import render_template,request,redirect,url_for
from create_app import app
from extensions import db
from models.user import User
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.reserved_parking_spot import ReservedParkingSpot
from datetime import datetime

@app.route('/book_lot_user/<user_name>/<login_success>/<lot_id>',methods=['POST','GET'])
def bookLotUser(user_name, login_success,lot_id):
    user=User.query.filter(User.username==user_name).first()
    lot=ParkingLot.query.filter(ParkingLot.id==lot_id).first()
    active_reserved_ids = db.session.query(ReservedParkingSpot.spot_id).filter(
    ReservedParkingSpot.reserved_status == True
    ).all()


    active_reserved_ids = [spot_id[0] for spot_id in active_reserved_ids]

    
    spot = ParkingSpot.query.filter(
    ParkingSpot.lot_id == lot_id,
    ParkingSpot.status == "A",
    ~ParkingSpot.id.in_(active_reserved_ids)  # NOT in list of reserved spots
    ).first()

    
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
    
    return render_template('User/book_lot_user.html',user_name=user_name, login_success=login_success,lot=lot,user=user,spot=spot) 