from flask import Flask
from .extensions import db, jwt
from .config import Config


def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.recipes import recipes_bp
    from app.routes.search import search_bp
    from app.routes.suggest import suggest_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(recipes_bp, url_prefix="/recipes")
    app.register_blueprint(search_bp, url_prefix="/recipes/search")
    app.register_blueprint(suggest_bp, url_prefix="/recipes/suggest")

    with app.app_context():
        db.drop_all()
        db.create_all()

    return app
