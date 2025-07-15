from flask import Flask
from extensions import db
from flask_migrate import Migrate

app = Flask(__name__)
migrate  = Migrate(app, db)

# flask db init
# flask db migrate -m " "
# flask db upgrade