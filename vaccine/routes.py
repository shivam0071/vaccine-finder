from flask import Blueprint, render_template, request
from flask import current_app  as app
from flask_mail import Message
from vaccine import util, constants, mail

vaccine = Blueprint('vaccine', __name__)

@vaccine.route("/status", methods=["GET"])
def status():
    app.logger.info("Loggers Initialized...")
    return ({"result": "The FLASK APP is running..."})


@vaccine.route("/index", methods=["GET"])
@vaccine.route('/')
def homepage():
    return render_template("index.html", data=constants.EMAIL_DATA)

@vaccine.route("/index", methods=["POST"])
@vaccine.route('/', methods=['POST'])
def find_vaccine_1():
    #  TODO: ADD VALIDATIONS
    pin = request.form['pincode']
    age = int(request.form['age'])
    if age < 45:
        age = 18
    else:
        age = 45

    vaccine_data = util.find_vaccine_deamon_helper([pin], [age])
    if vaccine_data:
        return {'result': vaccine_data}

    return {'result': 'failed'}

@vaccine.route("/send-vaccine-email/v1", methods=["GET"])
def send_email():
    try:
        html_template = render_template("email_template.html", data=len(constants.EMAIL_DATA))
        msg = Message('Vaccine Ping: Covid-19 Vaccine Available...', bcc=['']) # recipients here
        msg.html = html_template
        mail.send(msg)
        return {"Result": "Email Sent Successfully"}

    except Exception as ex:
        print("MAIL EXCEPTION", ex)
        return {"Result": "MAIL ERROR"}