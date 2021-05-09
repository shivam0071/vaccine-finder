import requests
import datetime
import time
from vaccine import constants
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl
from jinja2 import Environment, FileSystemLoader
import os
from config import Config

# SAMPLE DATA
EMAIL_PIN_AND_AGE = {
    'test@.com': {'400001': [18, 45]},
    }
# {'email':{'pincode':[age1, age2]}}

def get_pincode_and_age():
    global EMAIL_PIN_AND_AGE, EMAIL_DATA
    # call a method from DB or read from JSON/CSV for latest user data
    return EMAIL_PIN_AND_AGE

def find_vaccine_deamon_helper(pincode=[], age=[18]):
    start_date = datetime.datetime.now()
    vaccine_info = []
    center_found = False
    vaccine_day = start_date.strftime("%d-%m-%Y")
    for pin in pincode:
        print("*" * 20 + f" Scanning PINCODE - {pin} -- {age} " + "*" * 20)
        try:
            resp = requests.get(constants.BASE_URL.format(pin, vaccine_day), headers=constants.HEADERS)
            if resp.status_code != 200:
                print("COWIN API is DOWN")
                return
        except Exception as ex:
            print(f"Exception -- {ex} ")
            return

        center_info = resp.json().get('centers', [])
        if not center_info:
            print(f"Vaccination Center not found for PIN {pin}")

        for data in center_info:
            for session in data.get("sessions", []):
                if session.get('min_age_limit', 0) in age and session.get('available_capacity', 0) > 0:
                    pin_data = {"Center Name": data.get("name", "Unavailable"),
                     "Date": session['date'],
                     "Capacity Available": session['available_capacity'],
                     "Pincode": data.get("pincode", "NA"),
                     "Fee Type": data.get("fee_type", "NA"),
                     "Age Limit": session['min_age_limit'],
                     "Vaccine Type": session['vaccine']
                     }
                    vaccine_info.append(pin_data)
                    center_found = True
            if center_found:
                center_found = False
        print("*" * 20 + f" Scanning FINISHED for PIN - {pin} " + "*" * 20)

    return vaccine_info

def vaccination_thread():
    print("Starting Vaccination Deamon")
    global EMAIL_PIN_AND_AGE
    reset_cache_timer = constants.THREAD_REFRESH + 1
    while True:
        if reset_cache_timer < constants.THREAD_REFRESH:
            # check every 5 mins
            reset_cache_timer += 1
            time.sleep(1)
        else:
            constants.EMAIL_DATA = {}
            reset_cache_timer = 0
            EMAIL_PIN_AND_AGE = get_pincode_and_age()

            for user, details in EMAIL_PIN_AND_AGE.items():
                user_data = []
                for pin, age in details.items():
                    vaccine_info = find_vaccine_deamon_helper([pin], age)
                    if vaccine_info:
                         user_data.extend(vaccine_info)
                # 1 user complete
                constants.EMAIL_DATA[user] = user_data

            send_email(constants.EMAIL_DATA)

def send_email(email_data):

    smtp_server = Config.MAIL_SERVER
    port = Config.MAIL_PORT  # For starttls
    sender_email = Config.MAIL_USERNAME
    password = Config.MAIL_PASSWORD

    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        for email, value in email_data.items():
            if not value:
                print(f"***Email Data not found for email {email}***")
                continue
            message = MIMEMultipart()
            message["Subject"] = "Vaccine Ping: Covid-19 Vaccine Available..."
            message["From"] = f"{Config.MAIL_DEFAULT_SENDER}"
            message["Bcc"] = email

            env = Environment(
                loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__)))

            template = env.get_template('email_template.html')
            output = template.render(data=value)

            message.attach(MIMEText(output, "html"))
            msgBody = message.as_string()
            server.sendmail(sender_email, email, msgBody)
            time.sleep(2)

    except Exception as e:
        print(e)
    finally:
        server.quit()

if __name__ == "__main__":
    pass
