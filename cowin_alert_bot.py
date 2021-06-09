import requests
import time
import json
from datetime import date, timedelta
import telegram_send

URL1 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=571&date="
URL2 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=572&date="
URL3 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=565&date="

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def avail_check(slot_data, vac_name, vac_age, vac_dose):
    result_slots = []
    for item in slot_data:
        for session in item["sessions"]:
            if(session["min_age_limit"] == vac_age and session[vac_dose] > 0 and session["vaccine"]==vac_name):
                results = {}
                results["name"] = item["name"]
                results[vac_dose] = session[vac_dose]
                results["address"] = item["address"]
                results["pincode"] = item["pincode"]
                results["date"] = session["date"]
                results["vaccine"] = session["vaccine"]
                result_slots.append(results)
           
            elif(session["min_age_limit"] == vac_age or session[vac_dose] > 0):
                results = {}
                results["name"] = item["name"]
                results[vac_dose] = session[vac_dose]
                results["address"] = item["address"]
                results["pincode"] = item["pincode"]
                results["date"] = session["date"]
                results["vaccine"] = session["vaccine"]
                result_slots.append(results)

    return(result_slots)

vac_name = None
vac_age = 0
vac_dose = -1

while vac_name is None:
    name_param = input("Vaccine Name (Covishield/Covaxin): Leave blank if no preference \n")
    if(name_param.upper() in ["COVISHIELD", "COVAXIN", ""]):
        vac_name = name_param
    else:
        print("Incorrect Option, try again")

while vac_dose == -1:
    dose_param = input("Dose No (1/2): \n")
    if(dose_param in ["1", "2"]):
        vac_dose = "available_capacity_dose"+dose_param
    else:
        print("Incorrect Option, try again")

while vac_age == 0:
    age_param = input("Minimum Age: \n")
    if(age_param in ["18", "45"]):
        vac_age = int(age_param)
    else:
        print("Incorrect Option, try again")


while True:
    tom_date = (date.today() + timedelta(days=1)).strftime("%d-%m-%Y")
    
    # Checks slots for next 3 days of current date
    slot_tom = json.loads(requests.get(url = URL1+tom_date, headers = headers).text)
    slot_tom1 = json.loads(requests.get(url = URL2+tom_date, headers = headers).text)
    slot_tom2 = json.loads(requests.get(url = URL3+tom_date, headers = headers).text)
    
    slot_list = avail_check(slot_tom["centers"], vac_name, vac_age, vac_dose)
    slot_list2 = avail_check(slot_tom1["centers"], vac_name, vac_age, vac_dose)
    slot_list3 = avail_check(slot_tom2["centers"], vac_name, vac_age, vac_dose)

    message = ""
    for slot in slot_list+slot_list2+slot_list3:
        message += str(slot) + "\n"

    if(slot_list+slot_list2+slot_list3 != []):
        telegram_send.send(messages=[message])
        print(slot_list+slot_list2+slot_list3)
    else:
        print("No Slots Available")

    time.sleep(10)


