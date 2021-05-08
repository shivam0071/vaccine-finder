from logging.config import dictConfig
from flask import Flask
from config import Config
import config
import os
from flask_cors import CORS
from threading import Thread
from vaccine import util
from flask_mail import Mail


# extensions
cors = CORS()
mail = Mail()



def create_app(config_class=Config):
    app = Flask(__name__)

    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Dynamically load config based on the testing argument or FLASK_ENV environment variable
    flask_env = os.getenv("FLASK_ENV", None)
    if flask_env == "testing":
        app.config.from_object(config.TestingConfig)
        dictConfig(config.TestingConfig.LOGGING_BASE)
    elif flask_env == "development":
        app.config.from_object(config.DevelopmentConfig)
        dictConfig(config.DevelopmentConfig.DEVELOPMENT_LOGGING)
    else:
        app.config.from_object(config.ProductionConfig)
        dictConfig(config.ProductionConfig.PRODUCTION_LOGGING)

    # Init extensions here
    cors.init_app(app)
    mail.init_app(app)


    # Add blueprints here
    from vaccine.routes import vaccine
    app.register_blueprint(vaccine)

    # Threads Here
    thread = Thread(target=util.vaccination_thread, daemon=True)
    thread.start()

    return app