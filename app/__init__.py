from flask import Flask
from app.blueprints.auth.routes import auth_bp

from app.config import *

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DatabaseConfig().URI
    
    # Регистрация блюпринта auth
    app.register_blueprint(auth_bp, url_prefix='/')
    
    from app.models import db

    db.init_app(app)
    with app.app_context():
        db.Model.prepare(autoload_with=db.engine)

    return app
