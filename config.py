import os
from datetime import datetime


class Config:
    # Add configurations here
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get('SECRET_KEY',
                                "the_secret_key")  # for forms, prventing cross site attacks etc

    MAIL_SERVER = os.environ.get('MAIL_SERVER', "smtp.gmail.com")  # server of our email ID
    MAIL_PORT = int(os.environ.get('MAIL_PORT', "587"))
    MAIL_USE_TLS = True  # for security and encryption
    MAIL_USE_SSL = False  # for security and encryption
    # MAIL_DEBUG = False  # True if app[DEBUG] = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', "email_id_here")
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', "email_app_password")

    MAIL_DEFAULT_SENDER = ("Team: Find Vaccine", MAIL_USERNAME)  # default from sender
    MAIL_MAX_EMAILS = None  # prevent one mail call from sending too many emails
    # MAIL_SUPPRESS_SEND =  None # similar to debug...here its app[TESTING] = True
    MAIL_ASCII_ATTACHMENTS = False  # File names to ASCII

    # LOGGING
    LOGGING_BASE = {
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    }


class ProductionConfig(Config):
    PRODUCTION_LOGGING = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter': 'default',
                'level': 'INFO',
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/{:%Y%m%d-%H%M%S}.log'.format(datetime.now()),
                'formatter': 'default',
                'maxBytes': 10*1024*1024,
                'backupCount': 20,
                'level': 'DEBUG'
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        }
    }


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT_LOGGING = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter': 'default'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/{:%Y%m%d-%H%M%S}.log'.format(datetime.now()),
                'formatter': 'default',
                'maxBytes': 10 * 1024 * 1024,
                'backupCount': 20,
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }


class TestingConfig(Config):
    TESTING = True