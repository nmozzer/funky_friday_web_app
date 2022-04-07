from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 

db = SQLAlchemy()
migrate = Migrate(db)

import os

def create_app(test=False):
    app = Flask(__name__, static_folder='static')

    setup_error_handling(app)

    flask_env = os.getenv('FLASK_ENV', None)
    if test:
        app.config.from_object('config.TestConfig')
    elif flask_env == 'dev':
        app.config.from_object('config.DevConfig')
    elif flask_env == 'test':
        app.config.from_object('config.TestConfig')
    else:
        app.config.from_object('config.ProdConfig')

    init_plugins(app)

    with app.app_context():

        init_blueprints(app)
        return app

def init_plugins(app):
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

def init_blueprints(app):
    from .auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .systems.routes import system as system_blueprint
    app.register_blueprint(system_blueprint)

    from .improvements.routes import improvement as improvement_blueprint
    app.register_blueprint(improvement_blueprint)

    from .home.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

def setup_error_handling(app):
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, page_error)
def page_not_found(e):
    return render_template('404.html'), 404

def page_error(e):
    return render_template('500.html'), 500