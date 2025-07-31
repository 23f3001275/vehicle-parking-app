from flask import render_template
from create_app import app
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.admin import Admin

@app.route('/summary_admin/<admin_name>/<login_success>')
def summaryAdmin(admin_name, login_success):
    # Fetch the admin object
    admin = Admin.query.filter_by(username=admin_name).first()

    # Fetch all lots created by this admin
    lots = ParkingLot.query.filter_by(admin_id=admin.id).all()

    chart_data = []
    for lot in lots:
        total_spots = len(lot.spot_in_lot)
        reserved = sum(1 for spot in lot.spot_in_lot if spot.status and spot.status.upper() == 'R')
        occupied = sum(1 for spot in lot.spot_in_lot if spot.status and spot.status.upper() == 'O')
        available = total_spots - reserved - occupied

        chart_data.append({
            "reserved": reserved,
            "occupied": occupied,
            "available": available
        })

        lot.total_spots = total_spots
        lot.reserved_spots = reserved
        lot.occupied_spots = occupied
        lot.available_spots = available


    return render_template(
        "Admin/summary_admin.html",
        admin_name=admin_name,
        login_success=login_success,
        lots=lots,
        chart_data=chart_data
    )
