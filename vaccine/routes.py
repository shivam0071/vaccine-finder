from flask import Blueprint
from flask import current_app  as app

vaccine = Blueprint('vaccine', __name__)

@vaccine.route("/status", methods=["GET"])
def status():
    app.logger.info("Loggers Initialized...")
    return ({"result": "The FLASK APP is running..."})
