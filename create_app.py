from flask import Flask
from config import Config
from extensions import db
from flask_migrate import Migrate
app = Flask(__name__)
app.config.from_object(Config)
migrate  = Migrate(app, db)

# flask db init
# flask db migrate -m " "
# flask db upgrade