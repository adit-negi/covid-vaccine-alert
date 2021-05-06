import requests
import json
import smtplib, ssl
import time
from datetime import datetime, timedelta

def send_mail(subject, name):
    sender = 'your-email'
    s = smtplib.SMTP('smtp.gmail.com', 587)
  
    # start TLS for security
    s.starttls()
    print('here')
    
    # Authentication
    s.login("your-email", "your-password")
    
    # message to be sent
    message = subject + " "+ name
    
    # sending the mail
    s.sendmail("your-email", "sender-email", message)
    
    # terminating the session
    s.quit()

#Dates to start search, passed via query parameters
def get_dates(date):
    date2 = date
    day2 = date2.day
    month2 =date2.month
    year2 = date2.year
    if day2< 10:
        day2 = str(0)+ str(day2)
    else:
        day2 = str(day2)
    if month2<10: 
        month2 =str(0)+ str(month2)
    else:
        month2 = str(month2)
    date2 = day2+'-'+ month2+str(year2)
    return date2

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
pincode = input('input pincode you would like to search for')
while True:
    #search upto 2 weeks ahead
    date1, date2 = get_dates(datetime.now()), get_dates(datetime.now()+timedelta(days=7))
    for date in [date1, date2]:
        try:
            response =requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode='+ pincode + '&date='+date, headers = headers)
            response_json = json.loads(response.text)
            for center in response_json['centers']:
                for session in center['sessions']:
                    if session['available_capacity']>0 and session['min_age_limit']==18:
                        send_mail('Vaccine Slot Open Now', center['name'])
        except:
            continue
    
        #lets not throttle a govt site it hangs by a thread anyways
        time.sleep(300)



