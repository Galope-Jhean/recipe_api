from flask import Flask
from .extensions import db, jwt
from .config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.recipes import recipes_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(recipes_bp, url_prefix="/recipes")

    with app.app_context():
        db.drop_all()
        db.create_all()

    return app
