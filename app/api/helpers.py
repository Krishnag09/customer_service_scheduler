from flask import Flask, jsonify, url_for
from flask_mail import Mail, Message
import jwt , json
import datetime
import redis
from twilio.rest import Client
from app.config.config import Config


app = Flask(__name__)
app.config.from_object(Config)



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
       client.messages.create(to=phone_no, from_=twilio_default_from, body="Dear customer, Your service no is "+ service_no)
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
    # Start a transaction pipeline to ensure atomicity
    pipe = r.pipeline()

    # Check the length of the VIP list and pop if it has elements
    vip_length = pipe.llen('phone_vip')
    if vip_length > 0:
        next_customer_vip = pipe.rpop('phone_vip')
    else:
        # Check the length of the regular list and pop if it has elements
        reg_length = pipe.llen('phone_reg')
        if reg_length > 0:
            next_customer_reg = pipe.rpop('phone_reg')
        else:
            return "No customers in checkIn queue"

    # Execute the transaction
    responses = pipe.execute()

    # Process the results
    # The result of the rpop command for VIP
    if vip_length > 0 and responses[1]:
        next_customer_vip = responses[1].decode('utf-8')
        return json.dumps(next_customer_vip)
    elif responses[-1]:  # The result of the rpop command for regular
        next_customer_reg = responses[-1].decode('utf-8')
        return json.dumps(next_customer_reg)
    else:
        return "No customers in checkIn queue"
    
def next_customer_pro():
    pipe = r.pipeline()

    # Check if the counter exists, if not, set it to 0
    if not r.exists('vip_counter'):
        pipe.set('vip_counter', 0)

    # Get the counter value and check the length of the VIP list
    vip_counter = int(pipe.get('vip_counter').decode('utf-8'))
    vip_length = pipe.llen('phone_vip')

    # If conditions are met for VIP, pop a value and increment the counter
    if vip_length > 0 and vip_counter < 2:
        next_customer_vip = pipe.rpop('phone_vip')
        pipe.incr('vip_counter')
    else:
        # If conditions are met for regular, pop a value and reset the counter
        reg_length = pipe.llen('phone_reg')
        if reg_length > 0:
            next_customer_reg = pipe.rpop('phone_reg')
            pipe.set('vip_counter', 0)

    # Execute the transaction
    responses = pipe.execute()

    # The result of the rpop command for VIP
    if vip_length > 0 and vip_counter < 2 and responses[-2]:
        next_customer_vip = responses[-2].decode('utf-8')
        return json.dumps(next_customer_vip)
    elif responses[-1]:  # The result of the rpop command for regular
        next_customer_reg = responses[-1].decode('utf-8')
        return json.dumps(next_customer_reg)
    else:
        return "No customers in queue"
    
    
