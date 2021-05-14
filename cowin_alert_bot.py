import requests
import time
import json
from datetime import date, timedelta
import telegram_send

URL1 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=571&date="
URL2 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=572&date="
URL3 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=565&date="

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def avail_check(slot_data):
    result_slots = []
    for item in slot_data:
        for session in item["sessions"]:
            # if(session["min_age_limit"] == 18 and session["available_capacity"] > 0 and session["vaccine"]=="COVAXIN"):
            if(session["min_age_limit"] == 18 and session["available_capacity"] > 0):
                results = {}
                results["name"] = item["name"]
                results["address"] = item["address"]
                results["date"] = session["date"]
                results["vaccine"] = session["vaccine"]
                result_slots.append(results)

    return(result_slots)


while True:
    tom_date = (date.today() + timedelta(days=1)).strftime("%d-%m-%Y")


    slot_tom = json.loads(requests.get(url = URL1+tom_date, headers = headers).text)
    slot_tom1 = json.loads(requests.get(url = URL2+tom_date, headers = headers).text)
    slot_tom2 = json.loads(requests.get(url = URL3+tom_date, headers = headers).text)

    slot_list = avail_check(slot_tom["centers"])
    slot_list2 = avail_check(slot_tom1["centers"])
    slot_list3 = avail_check(slot_tom2["centers"])

    message = ""
    for slot in slot_list+slot_list2+slot_list3:
        message += str(slot) + "\n"

    if(slot_list+slot_list2+slot_list3 != []):
        telegram_send.send(messages=[message])


    print(slot_list+slot_list2+slot_list3)
    time.sleep(10)


