from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 
    
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nicksjm:postgres@localhost:5432/funky_friday'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import User, System, Improvement

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from .controllers.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .controllers.system import system as system_blueprint
app.register_blueprint(system_blueprint)

from .controllers.main import main as main_blueprint
app.register_blueprint(main_blueprint)


db.create_all()


