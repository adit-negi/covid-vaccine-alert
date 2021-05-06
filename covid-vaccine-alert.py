import requests
import json
import smtplib, ssl
import time
from datetime import datetime


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
pincode = input('input pincode you would like to search for')
while True:
    day = (datetime.now().day) 
    if day< 10:
        day = str(0)+ str(day)
    else:
        day = str(day)
    month = (datetime.now().month)
    if month<10: 
        month =str(0)+ str(month)
    else:
        month = str(month)
    year =str(datetime.now().year)
    date = day + '-' + month + '-' + year
    
    response =requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode='+ pincode + '&date='+date, headers = headers)
    response_json = json.loads(response.text)
    for center in response_json['centers']:
        for session in center['sessions']:
            if session['available_capacity']>0 and session['min_age_limit']>=18:
                send_mail('Vaccine Slot Open Now', center['name'])

    time.sleep(300)

def send_mail(subject, name):
    sender = 'your-email'
    s = smtplib.SMTP('smtp.gmail.com', 587)
  
    # start TLS for security
    s.starttls()
    
    # Authentication
    s.login("your-email", "your-password")
    
    # message to be sent
    message = subject + " "+ name
    
    # sending the mail
    s.sendmail("your-emai", "your-password", message)
    
    # terminating the session
    s.quit()


