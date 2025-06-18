from extensions import db
from sqlalchemy import CheckConstraint

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    fullname = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.Integer, CheckConstraint('pincode<1000000 AND pincode>99999'), comment='Indian PIN code (100001-999999)')
    reserved = db.relationship('ReservedParkingSpot', backref='u')

    def __repr__(self):
        return f'<User {self.username}>'