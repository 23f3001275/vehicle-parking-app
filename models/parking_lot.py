from app import db
from sqlalchemy import CheckConstraint

class ParkingLot(db.Model):
    __tablename__ = 'parkinglots'
    id = db.Column(db.Integer, primary_key=True, comment='ID of row in parkinglots table')
    prime_loc_name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.Integer, CheckConstraint('pincode<1000000 AND pincode>99999'), comment='Indian PIN code (100001-999999)')
    max_spots = db.Column(db.Integer, nullable=False)
    spot_in_lot = db.relationship('ParkingSpot', backref='pl')

class ParkingLot(db.Model):
    def __repr__(self):
        return f'<ParkingLot {self.id}: {self.prime_loc_name}>'