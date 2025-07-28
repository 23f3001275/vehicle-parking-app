from flask import render_template
from create_app import app
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.admin import Admin

@app.route('/home_admin/<admin_name>/<login_success>')
def homeAdmin(admin_name, login_success):
    # Get Admin object
    admin = Admin.query.filter(Admin.username==admin_name).first_or_404()
    
    lots = ParkingLot.query.filter_by(admin_id=admin.id).all()
    lot_data = []

    for lot in lots:
        occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status="O").count()
        available = ParkingSpot.query.filter_by(lot_id=lot.id, status="A").count()
        reserved = ParkingSpot.query.filter_by(lot_id=lot.id, status="R").count()

        lot_data.append({
            'lot': lot,
            'occupied': occupied,
            'available': available,
            'reserved': reserved
        })

    return render_template(
        'Admin/home_admin.html',
        admin_name=admin_name,
        login_success=login_success,
        lot_data=lot_data
    )
