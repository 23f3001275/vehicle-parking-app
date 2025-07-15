from extensions import db
# from datetime import datetime, timezone

class ReservedParkingSpot(db.Model):
    __tablename__ = 'reservedparkingspots'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parkingspots.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    reserve_timestamp = db.Column(db.DateTime, nullable=False)
    park_timestamp = db.Column(db.DateTime, nullable=True)
    leave_timestamp = db.Column(db.DateTime, nullable=True)
    park_cost_per_unit_time = db.Column(db.Integer, nullable=True)
    reserve_status = db.Column(db.Boolean, nullable=False)
    vehicle_no = db.Column(db.String(10), nullable=False)
    # False = INACTIVE, To be seen in recent history
    # True = ACTIVE, It is currently reserved/occupied

    def __repr__(self):
        return f'<Reservation {self.id}: User {self.user_id} -> Spot {self.spot_id}>'
    
# default=datetime.now(timezone.utc)