from flask import render_template
from create_app import app
from extensions import db
from models.user import User
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.reserved_parking_spot import ReservedParkingSpot
from sqlalchemy import func
from datetime import datetime
import calendar

@app.route('/summary_user/<user_name>/<login_success>')
def summaryUser(user_name, login_success):
    user = User.query.filter_by(username=user_name).first()
    if not user:
        return "User not found", 404

    now = datetime.now()
    month_map = {f"{i:02}": calendar.month_abbr[i] for i in range(1, 13)}

    # 1. Monthly reservation count
    monthly_counts = (
        db.session.query(
            func.strftime('%m', ReservedParkingSpot.reserve_timestamp),
            func.count()
        )
        .filter(ReservedParkingSpot.user_id == user.id)
        .group_by(func.strftime('%m', ReservedParkingSpot.reserve_timestamp))
        .order_by(func.strftime('%m', ReservedParkingSpot.reserve_timestamp))
        .all()
    )
    monthly_labels = [month_map.get(m, m) for m, _ in monthly_counts]
    monthly_values = [v for _, v in monthly_counts]

    # 2. Monthly cost summary
    monthly_costs = (
        db.session.query(
            func.strftime('%m', ReservedParkingSpot.reserve_timestamp),
            func.sum(ReservedParkingSpot.park_cost_per_unit_time)
        )
        .filter(ReservedParkingSpot.user_id == user.id)
        .group_by(func.strftime('%m', ReservedParkingSpot.reserve_timestamp))
        .order_by(func.strftime('%m', ReservedParkingSpot.reserve_timestamp))
        .all()
    )
    cost_labels = [month_map.get(m, m) for m, _ in monthly_costs]
    cost_values = [float(c or 0) for _, c in monthly_costs]

    # 3. Reservations by parking lot
    lot_counts = (
        db.session.query(
            ParkingLot.prime_loc_name,
            func.count()
        )
        .join(ParkingSpot, ParkingLot.id == ParkingSpot.lot_id)
        .join(ReservedParkingSpot, ReservedParkingSpot.spot_id == ParkingSpot.id)
        .filter(ReservedParkingSpot.user_id == user.id)
        .group_by(ParkingLot.prime_loc_name)
        .all()
    )
    lot_labels = [lot for lot, _ in lot_counts]
    lot_values = [count for _, count in lot_counts]

    # 4. Status breakdown (Completed vs Ongoing)
    reservations = ReservedParkingSpot.query.filter_by(user_id=user.id).all()
    status_map = {'Ongoing': 0, 'Completed': 0}
    for r in reservations:
        if r.leave_timestamp is None or r.leave_timestamp > now:
            status_map['Ongoing'] += 1
        else:
            status_map['Completed'] += 1
    status_labels = list(status_map.keys())
    status_values = list(status_map.values())

    # 5. Weekly reservation trend
    weekly_counts = (
        db.session.query(
            func.strftime('%W', ReservedParkingSpot.reserve_timestamp),
            func.count()
        )
        .filter(ReservedParkingSpot.user_id == user.id)
        .group_by(func.strftime('%W', ReservedParkingSpot.reserve_timestamp))
        .order_by(func.strftime('%W', ReservedParkingSpot.reserve_timestamp))
        .all()
    )
    week_labels = [f"Week {int(w)}" for w, _ in weekly_counts]
    week_values = [v for _, v in weekly_counts]

    # 6. Reservations by location (prime location name)
    location_counts = (
        db.session.query(
            ParkingLot.prime_loc_name,
            func.count()
        )
        .join(ParkingSpot, ParkingLot.id == ParkingSpot.lot_id)
        .join(ReservedParkingSpot, ReservedParkingSpot.spot_id == ParkingSpot.id)
        .filter(ReservedParkingSpot.user_id == user.id)
        .group_by(ParkingLot.prime_loc_name)
        .all()
    )
    location_labels = [loc for loc, _ in location_counts]
    location_values = [count for _, count in location_counts]

    # Prepare chart data dictionary
    data = {
        'monthly': {'labels': monthly_labels, 'values': monthly_values},
        'cost': {'labels': cost_labels, 'values': cost_values},
        'lot': {'labels': lot_labels, 'values': lot_values},
        'status': {'labels': status_labels, 'values': status_values},
        'weekly': {'labels': week_labels, 'values': week_values},
        'location': {'labels': location_labels, 'values': location_values},
    }

    return render_template(
        'user/summary_user.html',
        user_name=user_name,
        login_success=login_success,
        data=data
    )
