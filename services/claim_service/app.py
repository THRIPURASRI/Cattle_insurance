from flask import Flask
from extensions import db
from routes import claim_routes
import os

app = Flask(__name__)
app.secret_key = 'your_claim_secret_key'

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'db.sqlite3')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(app)

from models import Claim

# Register routes
app.register_blueprint(claim_routes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5003, debug=True)