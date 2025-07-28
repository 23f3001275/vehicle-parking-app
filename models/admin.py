from extensions import db

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)
    lot_maker = db.relationship('ParkingLot', backref='a')

    def __repr__(self):
        return f'<Admin {self.username}>'
    
# # To add predefined admin using terminal
# flask shell
# >>> from create_app import app
# >>> from models.admin import Admin
# >>> new_admin = Admin(username='RKS', password='010305')
# >>> db.session.add(new_admin)
# >>> db.session.commit()
# >>> exit()