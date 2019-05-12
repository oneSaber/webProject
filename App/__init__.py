from flask import Flask
from Config import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config["development"])

    from .Model import db
    db.init_app(app)

    from .main import main_blueprint as main
    app.register_blueprint(main)

    from .Course import course_blueprint as course
    app.register_blueprint(course)

    from .Model import login_manager
    login_manager.init_app(app)
    return app

