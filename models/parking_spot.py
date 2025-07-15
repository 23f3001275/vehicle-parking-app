from extensions import db

class ParkingSpot(db.Model):
    __tablename__ = 'parkingspots'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parkinglots.id', ondelete='CASCADE'))
    status = db.Column(db.String(1), default="A", nullable=False) 
    reserved_spot = db.relationship('ReservedParkingSpot', backref='ps')

    def __repr__(self):
        return f'<ParkingSpot {self.id} (Lot: {self.lot_id})>'