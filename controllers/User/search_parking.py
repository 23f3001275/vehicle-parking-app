from flask import render_template,request
from create_app import app
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from sqlalchemy import or_

@app.route('/search_parking/<user_name>/<login_success>', methods=['POST', 'GET'])
def searchParking(user_name, login_success):
    lots = ParkingLot.query.all()
    lot_data = None
    lot_data_1 = []

    if request.method == 'POST':
        search_name = request.form.get('loc_name', '').strip()
        lot_id = request.form.get('lot_id', '')

        # Priority: dropdown search if selected, else text search
        if lot_id:
            lot_data = ParkingLot.query.filter_by(id=lot_id).all()
        elif search_name:
            lot_data = ParkingLot.query.filter(ParkingLot.prime_loc_name.ilike(f"%{search_name}%")).all()

        if lot_data:
            for lot in lot_data:
                occupied_or_reserved = ParkingSpot.query.filter(
                    ParkingSpot.lot_id == lot.id,
                    or_(ParkingSpot.status == "O", ParkingSpot.status == "R")
                ).count()
                full = occupied_or_reserved == lot.max_spots
                lot_data_1.append({
                    "lot": lot,
                    "full": full
                })

    return render_template(
        'User/search_parking_user.html',
        user_name=user_name,
        login_success=login_success,
        lots=lots,
        lot_data=lot_data,
        lot_data_1=lot_data_1
    )
