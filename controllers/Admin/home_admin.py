from flask import render_template
from create_app import app
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot

@app.route('/home_admin/<admin_name>/<login_success>')
def homeAdmin(admin_name,login_success):
    lots = ParkingLot.query.all()
    lot_data = []
    for lot in lots:
        occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status=True).count()
        available = ParkingSpot.query.filter_by(lot_id=lot.id, status=False).count()

        lot_data.append({
            'lot': lot,
            'occupied': occupied,
            'available': available
        })

    return render_template("Admin/home_admin.html", admin_name=admin_name, login_success=login_success, lot_data=lot_data)