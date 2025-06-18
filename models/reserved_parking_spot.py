from extensions import db
# from datetime import datetime, timezone

class ReservedParkingSpot(db.Model):
    __tablename__ = 'reservedparkingspots'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parkingspots.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    park_timestamp = db.Column(db.DateTime, nullable=False)
    leave_timestamp = db.Column(db.DateTime, nullable=False)
    park_cost_per_unit_time = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Reservation {self.id}: User {self.user_id} -> Spot {self.spot_id}>'
    
# default=datetime.now(timezone.utc)