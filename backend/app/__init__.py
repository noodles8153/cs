from flask import Flask
from .extensions import db, jwt
from .routes import frp_router, auth_router
from .config import default

def create_app(config=default):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(frp_router, url_prefix='/api/frp')
    app.register_blueprint(auth_router, url_prefix='/api/auth')

    return app