from flask import Flask, jsonify, url_for
from flask_mail import Mail, Message
import jwt
import datetime
import redis
from twilio.rest import Client
from app.config.config import Config


app = Flask(__name__)

# Flask-Mail configuration
# Use your email provider's SMTP server
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


mail = Mail(app)

SECRET_KEY = "test_secret_key"

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def generate_token(email):
    # Create a unique token
    expiration = datetime.datetime.utcnow(
    ) + datetime.timedelta(minutes=15)  # Token valid for 15 minutes

    token = jwt.encode({'email': email, 'exp': expiration},
                       SECRET_KEY, algorithm='HS256')
    return token

def generate_service_no(phone_no):
    #Create a sequential service number
    try: 
        if r.get('service_no') is None:
            r.set('service_no', 0)
        service_no = r.incr('service_no')
        return "Your service number is: " + str(service_no)
    except:
        return "Error generating service number, please try again later"

def store_service_no(phone_no, service_no):
    #Store the service number against the phone number
    try:
        r.set(phone_no, service_no)
        return 'The service number has been stored against the phone number'
    except:
        return 'Error storing service number, please try again later'
    
def send_sms(phone_no, service_no):
    #Send the service number to the phone number using twilio
    client = Client(Config.twilio_account_sid, Config.twilio_auth_token)
    if phone_no:
       twilio_default_from = Config.twilio_default_from
       return("sms test pass")
    #    message = client.messages.create(
    #                  body="Join Earth's mightiest heroes. Like Kevin Bacon.",
    #                  from_='+15017122661',
    #                  to='+18019468704'
    #              )

    else:
        return 'Please enter a valid phone number'
    
def checkIn(customer):
    # push_to_queue(phone_no)
    r_list = r.lrange('queue', 0, -1)
    p_list = r.lrange('phone_no', 0, -1)
    if customer.VIP == True:
        p_list.push(customer.phone_no)
    else:
        r_list.push(customer.phone_no)
    return 'You have been checked in'
    
def getNextCustomer(phone_no, p_list, r_list):
    # helps provide the next customer in the queue
    if p_list is not None:
        next_customer = p_list.pop()
    else:
        next_customer = r_list.pop()
    return next_customer

