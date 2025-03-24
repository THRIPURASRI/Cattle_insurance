from flask import Flask
from extensions import db, login_manager
import os

app = Flask(__name__)
app.secret_key = 'THNKKOLPLLMM234rNBGFGDFGGJHJKKJKJKKLKLKKLKYYFDXDFS'

# Config
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'db.sqlite3')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth_routes.login'

# Import after app and db are set up
from models import User
from routes import auth_routes

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_routes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=True)
