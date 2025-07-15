from flask import render_template
from create_app import app
from extensions import db
from models.user import User
from models.parking_spot import ParkingSpot
from models.parking_lot import ParkingLot
from models.reserved_parking_spot import ReservedParkingSpot
from sqlalchemy import func
import calendar

@app.route('/summary_user/<user_name>/<login_success>')
def summaryUser(user_name, login_success):
    user = User.query.filter_by(username=user_name).first()

    # Month map
    month_map = {f"{i:02}": calendar.month_abbr[i] for i in range(1, 13)}

    # Monthly reservation count
    monthly_counts = (
        db.session.query(func.strftime('%m', ReservedParkingSpot.reserve_timestamp), func.count())
        .filter(ReservedParkingSpot.user_id == user.id)
        .group_by(func.strftime('%m', ReservedParkingSpot.reserve_timestamp))
        .order_by(func.strftime('%m', ReservedParkingSpot.reserve_timestamp))
        .all()
    )
    labels = [month_map.get(m, m) for m, _ in monthly_counts]
    values = [v for _, v in monthly_counts]

    # Monthly cost
    monthly_costs = (
        db.session.query(func.strftime('%m', ReservedParkingSpot.reserve_timestamp), func.sum(ReservedParkingSpot.park_cost_per_unit_time))
        .filter(ReservedParkingSpot.user_id == user.id)
        .group_by(func.strftime('%m', ReservedParkingSpot.reserve_timestamp))
        .order_by(func.strftime('%m', ReservedParkingSpot.reserve_timestamp))
        .all()
    )
    cost_labels = [month_map.get(m, m) for m, _ in monthly_costs]
    cost_values = [float(c) for _, c in monthly_costs]

    # Reservation by lot
    lot_counts = (
        db.session.query(ParkingLot.prime_loc_name, func.count())
        .join(ParkingSpot, ParkingLot.id == ParkingSpot.lot_id)
        .join(ReservedParkingSpot, ReservedParkingSpot.spot_id == ParkingSpot.id)
        .filter(ReservedParkingSpot.user_id == user.id)
        .group_by(ParkingLot.id)
        .all()
    )
    lot_labels = [name for name, _ in lot_counts]
    lot_values = [count for _, count in lot_counts]

    # Reservation status
    status_counts = (
    db.session.query(
        ReservedParkingSpot.reserve_status,
        func.count()
    )
    .filter(ReservedParkingSpot.user_id == user.id)
    .group_by(ReservedParkingSpot.reserve_status)
    .all()
)

    # Convert to labels
    status_labels = ['Active' if s else 'Inactive' for s, _ in status_counts]
    status_values = [count for _, count in status_counts]


    weekly_counts = (
    db.session.query(
        func.strftime('%W', ReservedParkingSpot.reserve_timestamp).label('week'),
        func.count().label('count')
    )
    .filter(ReservedParkingSpot.user_id == user.id)
    .group_by('week')
    .order_by('week')
    .all()
)

    week_labels = [f"Week {int(w)}" for w, _ in weekly_counts]
    week_values = [c for _, c in weekly_counts]

    location_counts = (
    db.session.query(
        ParkingLot.prime_loc_name,
        func.count().label('count')
    )
    .join(ParkingSpot, ParkingLot.id == ParkingSpot.lot_id)
    .join(ReservedParkingSpot, ReservedParkingSpot.spot_id == ParkingSpot.id)
    .filter(ReservedParkingSpot.user_id == user.id)
    .group_by(ParkingLot.prime_loc_name)
    .all()
)

    loc_labels = [name for name, _ in location_counts]
    loc_values = [count for _, count in location_counts]



    return render_template(
        'user/summary_user.html',
        user_name=user_name,
        login_success=login_success,
        data={
            'monthly': {'labels': labels, 'values': values},
            'cost': {'labels': cost_labels, 'values': cost_values},
            'lot': {'labels': lot_labels, 'values': lot_values},
            'status': {'labels': status_labels, 'values': status_values},
            'weekly': {'labels': week_labels, 'values':week_values},
            'location': {'labels':loc_labels, 'values':loc_values}
        }
    )
