from flask import Flask
from app.blueprints.auth.routes import auth_bp

def create_app():
    app = Flask(__name__)
    
    # Регистрация блюпринта auth
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
