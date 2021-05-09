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
    return {'result': "Vaccines Are Fully Booked"}


@vaccine.route("/vaccine-email", methods=["GET"])
def send_email():
    try:
        for email, value in constants.EMAIL_DATA.items():
            msg = Message('Vaccine Ping: Covid-19 Vaccine Available...', bcc=[email]) # recipients here
            if not value:
                print(f"***Email Data not found for email {email}***")
                continue
            html_template = render_template("email_template.html", data=value)
            msg.html = html_template
            mail.send(msg)

        return {"Result": "API ran Successfully"}

    except Exception as ex:
        print("MAIL EXCEPTION", ex)
        return {"Result": "MAIL ERROR"}