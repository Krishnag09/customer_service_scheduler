from flask import request, Flask
from flask_restful import Resource
from .helpers import generate_service_no, store_service_no, send_sms, check_in, next_customer, next_customer_pro
import json

app = Flask(__name__)


class HelloWorld(Resource):
    def get(self):
        return 'Hello, World! This is the Scheduler!'
    
class ServiceScheduler(Resource):
    def get(self):
        return 'Hello, World! This is the Scheduler !'
    def post(self):
        client = next_customer() # get the next customer from the queue
        if client: 
            service_no = generate_service_no(client)
            store_service_no(client, service_no)
            # send_sms(client, service_no)
            return "Service number for "+ str(client) +"is: "+ str(service_no)
        else:
            return 'No customers found in the check in list'
class ServiceSchedulerPro(Resource):
    def get(self):
        return 'Hello, World! This is the Pro Scheduler !'
    def post(self):
        client = next_customer_pro() # get the next customer from the queue
        if client: 
            service_no = generate_service_no(client)
            store_service_no(client, service_no)
            # send_sms(client, service_no)
            return 'Your service number is: ' + service_no
        else:
            return 'Customer not found in the check in list'
    
class CheckIn(Resource):
    def get(self):
        return 'Hello, World! This is the CheckIn!'
    def post(self):
        client_phone = request.json['client_phone']
        check_in(client_phone)
        return "You have been checked in"
        
