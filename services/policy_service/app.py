from flask import Flask
from extensions import db
from routes import policy_routes
import os

app = Flask(__name__)
app.secret_key = 'your_policy_secret_key'

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'db.sqlite3')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(app)

# Import models after db is initialized
from models import Policy, UserPolicy

# Register routes
app.register_blueprint(policy_routes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5002, debug=True)