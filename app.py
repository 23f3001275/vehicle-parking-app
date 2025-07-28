from flask import render_template
from create_app import app
from extensions import db
from controllers.User import *
from controllers.Admin import *

db.init_app(app)

@app.route('/')
def landing_page():
    return render_template("landing_page.html")

def create_default_admin():
    from models.admin import Admin

    existing_admin = Admin.query.filter_by(username="admin").first()
    if not existing_admin:
        new_admin = Admin(username="admin", password="pass123")
        db.session.add(new_admin)
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_default_admin()
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