from flask import render_template
from create_app import app
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.admin import Admin


@app.route('/summary_admin/<admin_name>/<login_success>')
def summaryAdmin(admin_name, login_success):
    # Get all lots created by this admin
    admin = Admin.query.filter_by(username=admin_name).first();
    lots = ParkingLot.query.filter(ParkingLot.admin_id==admin.id).all()
    chart_data = []
    for lot in lots:
        total = len(lot.spot_in_lot)
        reserved = sum(1 for spot in lot.spot_in_lot if spot.status == 'reserved')
        available = total - reserved
        chart_data.append({
            "reserved": reserved,
            "available": available
        })
    return render_template("Admin/summary_admin.html",
                           admin_name=admin_name,
                           login_success=login_success,
                           lots=lots,
                           chart_data=chart_data)
