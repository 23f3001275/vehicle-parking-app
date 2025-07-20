from flask import render_template,request,redirect,url_for
from create_app import app
from extensions import db
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
@app.route('/edit_lot/<admin_name>/<login_success>/<lot_id>',methods=['POST','GET'])
def editLot(admin_name,login_success,lot_id):    
    lot = ParkingLot.query.filter(ParkingLot.id==lot_id).first()
    if request.method=='POST':
        lot.prime_loc_name=request.form['loc_name']
        lot.price=request.form['price']
        lot.max_spots=request.form['max_spots']
        lot.address=request.form['address']
        lot.pincode=request.form['pincode']


        new_max = int(request.form['max_spots'])
        existing_count = ParkingSpot.query.filter_by(lot_id=lot.id).count()

        if new_max > existing_count:
            for _ in range(new_max - existing_count):
                new_spot = ParkingSpot(lot_id=lot.id, status="A")
                db.session.add(new_spot)
        elif new_max < existing_count:  
            removable = ParkingSpot.query.filter_by(lot_id=lot.id, status="A").limit(existing_count - new_max).all()
            for spot in removable:
                db.session.delete(spot)

       
        try:
            db.session.commit()
            return redirect(url_for('homeAdmin',admin_name=admin_name,login_success=login_success))
        except:
            return "there was problem editing the lot"   
    return render_template('Admin/edit_lot.html',login_success=login_success,admin_name=admin_name,lot=lot)