from flask import render_template
from create_app import app
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot

@app.route('/display_lot/<admin_name>/<login_success>/<lot_id>')
def displayLot(admin_name, login_success, lot_id):
    lot = ParkingLot.query.filter_by(id=lot_id).first_or_404()
    lot_data = []
    occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status=True).count()
    available = ParkingSpot.query.filter_by(lot_id=lot.id, status=False).count()

    lot_data.append({
        'lot': lot,
        'occupied': occupied,
        'available': available
    })

    return render_template('Admin/display_lot.html', admin_name=admin_name, login_success=login_success,lot_data=lot_data)