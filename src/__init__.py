from flask import Flask, render_template
from flask_cors import CORS

from src.config import Config
# from src.api import api
from src.extensions import db, api, migrate, jwt
from src.views import test_blueprint
from src.commands import init_db, populate_db, insert_db

from src.models import Center

# from src.models import User

BLUEPRINTS = [test_blueprint]
COMMANDS = [init_db, populate_db, insert_db]


def create_app(config=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config)

    @app.route('/')
    def index():
        cities = Center.query.all()
        print(cities)
        return render_template('index.html')
    
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_error_handlers(app)

    return app


def register_extensions(app):

    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Migrate
    migrate.init_app(app, db)

    # Flask-restX
    api.init_app(app)

    # Flask-JWT-Extended
    jwt.init_app(app)

    # @jwt.user_identity_loader
    # def user_identity_lookup(user):
    #     try:
    #         return user.uuid
    #     except AttributeError:
    #         return user
        
    # @jwt.user_lookup_loader
    # def user_lookup_callback(_jwt_header, jwt_data):
    #     user_uuid = jwt_data.get("sub")
    #     # print(f"JWT Data: {jwt_data}")
    #     if user_uuid:
    #         user = User.query.filter_by(uuid=user_uuid).first()
    #         return user
    #     return None
    
def register_blueprints(app):
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)
    
def register_commands(app):
    for command in COMMANDS:
        app.cli.add_command(command)
        
# Custom error handler for 404
def register_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        # You can return a JSON response or render a custom HTML template
        return render_template('404.html'), 404
    
    