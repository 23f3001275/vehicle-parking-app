from flask import Flask,render_template,request,redirect,url_for,session
from create_app import app, migrate
from extensions import db
from models import User
from controllers.User import *
from controllers.Admin import *

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db.init_app(app)

@app.route('/')
def landing_page():
    return render_template("landing_page.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# # Re-initalize database
# >>> from create_app import app
# >>> from extensions import db
# >>> with app.app_context():
# ...     db.create_all()
# ... 
# >>> exit()


# # Only drop specific table data
# >>> from extensions import db
# >>> from models.file import ClassName
# >>> db.session.query(ClassName).delete()
# >>> db.session.commit()
# >>> exit()