from flask import render_template
from create_app import app
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot

@app.route('/display_lot/<admin_name>/<login_success>/<lot_id>')
def displayLot(admin_name, login_success, lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    lot_data=[]
    occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status="O").count()
    available = ParkingSpot.query.filter_by(lot_id=lot.id, status="A").count()
    reserved = ParkingSpot.query.filter_by(lot_id=lot.id, status="R").count()
    lot_id=lot.id
    lot_data.append({
        'lot': lot,
        'occupied': occupied,
        'available': available,
        'lot_id':lot_id,
        'reserved':reserved
    })
    return render_template('Admin/display_lot.html',admin_name=admin_name, login_success=login_success,lot=lot,lot_id=lot_id,lot_data=lot_data) 