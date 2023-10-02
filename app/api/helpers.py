from flask import Flask, jsonify, url_for
from flask_mail import Mail, Message
import jwt , json
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


with open('app/api/customers.json', 'r') as json_file:
    data = json.load(json_file)


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
    
def check_in(phone):
    # push_to_queue(phone_no)
    customer = data['customers'].get(phone)
    if customer.get('vip'):
        r.lpush('phone_vip', phone) # push as the last element the list
        print("VIP customer checked in", phone)
    else:
        r.lpush('phone_reg', phone)
        print ("Regular customer checked in", phone)
    return 'You have been checked in'
    
def next_customer():
    # helps provide the next customer in the queue
    if r.llen('phone_vip') > 0:
        next_customer = r.rpop('phone_vip') # pop the first element from the list
        next_customer = next_customer.decode('utf-8')
        print("VIP customer queued", next_customer)
        return json.dumps(next_customer)
        # add all/partial queue empty logic here
    elif r.llen('phone_reg') > 0:
        next_customer_2 = r.rpop('phone_reg')
        next_customer_2 = next_customer_2.decode('utf-8')
        print ("Regular customer queued", next_customer_2)
        return json.dumps(next_customer_2)
    else:
        return "No customers in queue"
    
def next_customer_pro():
    #process VIP customers at double the rate of regular customers
    if r.get('vip_counter') is None:
            r.set('vip_counter', 0)
    vip_counter = int(r.get('vip_counter').decode('utf-8'))
    if r.llen('phone_vip') > 0 and vip_counter < 2:
        next_customer = r.rpop('phone_vip')
        r.incr('vip_counter')
        next_customer = next_customer.decode('utf-8')
        return json.dumps(next_customer)
    elif r.llen('phone_reg') > 0:
        next_customer_2 = r.rpop('phone_reg')
        next_customer_2 = next_customer_2.decode('utf-8')
        r.set('vip_counter', 0)
        return json.dumps(next_customer_2)
    
    
