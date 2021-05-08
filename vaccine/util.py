import requests
import datetime
import time
from vaccine import constants
from flask import current_app as app

# SAMPLE DATA
EMAIL_PIN_AND_AGE = {
    'test@.com': {'400001': [18, 45]},
    }
# {'email':{'pincode':[age1, age2]}}

def find_vaccine(pincode=None):

    start_date = datetime.datetime.now()
    # for days in range(no_of_days):
    # import pdb
    # pdb.set_trace()
    vaccine_day = start_date.strftime("%d-%m-%Y")
    try:
        resp = requests.get(constants.BASE_URL.format(pincode, vaccine_day), headers=constants.HEADERS)
        if resp.status_code != 200:
            print("COWIN API is DOWN")
            return
    except Exception as ex:
        print(f"Exception -- {ex} ")
        return

    center_info = resp.json().get('centers', [])
    for data in center_info:
        print("Center Name: {}\nFee Type: {}".format(data.get("name", "Unavailable"), data.get("fee_type", "NA")))
        for session in data.get("sessions", []):
            print("Date: {}\nCapacity Available: {}\nAge Limit: {}\nVaccine: {}".
                  format(session['date'], session['available_capacity'], session['min_age_limit'], session['vaccine']))
        print("*" * 50)
    # start_date += datetime.timedelta(days=1)

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
                if session.get('min_age_limit', 0) in age and session.get('available_capacity', 0) >= 0:
                    info1 = "Center Name: {} Fee Type: {} Pincode: {}".\
                        format(data.get("name", "Unavailable"), data.get("fee_type", "NA"), data.get("pincode", "NA"))
                    info2 = " Date: {} Capacity Available: {} Age Limit: {} Vaccine: {}".\
                        format(session['date'], session['available_capacity'], session['min_age_limit'], session['vaccine'])
                    vaccine_info.append(info1 + info2)
                    center_found = True
            if center_found:

                center_found = False
        print("*" * 20 + f" Scanning FINISHED for PIN - {pin} " + "*" * 20)

    # app.logger.info(f"PIN - {pincode}  AGE - {age}")
    # app.logger.info(f"Vaccine Info - {vaccine_info}")
    return vaccine_info

def vaccination_thread():
    app.logging.info("Starting Vaccination Deamon")
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
                for pin, age in details.items():
                    constants.EMAIL_DATA[user] = find_vaccine_deamon_helper([pin], age)


if __name__ == "__main__":
    pass
