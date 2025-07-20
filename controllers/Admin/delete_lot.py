from flask import render_template,request,redirect,url_for
from create_app import app
from extensions import db
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot

@app.route('/delete_lot/<admin_name>/<login_success>/<lot_id>',methods=['POST','GET'])
def deleteLot(admin_name,login_success,lot_id):    
    lot = ParkingLot.query.filter(ParkingLot.id==lot_id).first()
    available = ParkingSpot.query.filter_by(lot_id=lot.id, status="A").count()
    if lot.max_spots==available:
        try:
            db.session.delete(lot)
            db.session.commit()
            return redirect(url_for('homeAdmin',admin_name=admin_name,login_success=login_success))
        except:
            return "there was problem deleting the lot"  
    else:
        return "there are some booked spots"
    
    return redirect(url_for('home_admin',admin_name=admin_name,login_success=login_success))