from flask import request, Flask
from flask_restful import Resource
from .helpers import generate_service_no, store_service_no, send_sms
import json

app = Flask(__name__)


class HelloWorld(Resource):
    def get(self):
        return 'Hello, World! This is the Scheduler!'
    
class ServiceScheduler(Resource):
    def get(self):
        return 'Hello, World! This is the Scheduler get!'
    def post(self):
        client_phone = request.json['client_phone']
        with open('app/api/customers.json', 'r') as json_file:
            data = json.load(json_file)
        client=data['customers'].get(client_phone)
        if client: 
            service_no = generate_service_no(client_phone)
            print(service_no)
            store_service_no(client_phone, service_no)
            send_sms(client_phone, service_no)
            return 'Your service number is: ' + service_no
        else:
            return 'No record found for this phone number'


# class providerSchedule(Resource):
#     def post(self):
#         provider_id= request.json['provider_id']
#         date = request.json['date']
#         start_time = request.json['start_time']
#         end_time = request.json['end_time']
#         start_time_obj = datetime.datetime.strptime(start_time, '%H:%M').time()
#         end_time_obj = datetime.datetime.strptime(end_time, '%H:%M').time()  
#         start_time_slot = int((start_time_obj.hour*60 + start_time_obj.minute)/15)
#         end_time_slot = int((end_time_obj.hour*60 + end_time_obj.minute)/15)
#         slots= [i for i in range(start_time_slot, end_time_slot)]
#         schedule_dict = {
#             provider_id: {
#                 date: slots}
#         }
#         with open('app/api/providers.json', 'w') as json_file:
#             json.dump(schedule_dict, json_file, indent=4)
#         return 'Your schedule has been saved!'

# class clientSchedule(Resource):
#     def post(self):
#         date = request.json.get('date')
#         provider_id = str(request.json['provider_id'])
#         client_id = str(request.json['client_id'])
#         requested_slot= request.json['requested_slot']
#         print(requested_slot)
#         with open('app/api/providers.json', 'r') as json_file:
#             data = json.load(json_file)
#         print(data)
#         # checking if the requested slot is available
#         print(data.get(provider_id).get(date))
#         try:
#             if requested_slot in data.get(provider_id).get(date):
#                 client_email = data.get(client_id).get('email')
#                 token = generate_token(client_email)
#                 redis_save = {
#                     'provider_id': provider_id,
#                     'date': date,
#                     'requested_slot': requested_slot,
#                 }
#                 # saving the booking details on redis using the token as the key
#                 save_on_redis(token, redis_save)
#                 # sending the verification email
#                 send_verification(client_email, token)
#                 return 'Hello, World! This is the Scheduler post!'
#             else:
#                 return 'The requested slot is not availables'
#         except Exception as Excep :
#             print(Excep)
        
# class verifyBooking(Resource):
#     def get(self):
#         token = request.args.get('token')
#         r = redis.Redis()
#         # getting the booking details from redis
#         redis_data = r.hgetall(token)
#         redis_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in redis_data.items()}
        
#         provider_id = redis_data.get('provider_id')
#         date = redis_data.get('date')
#         requested_slot = redis_data.get('requested_slot')
#         with open('app/api/providers.json', 'r') as json_file:
#             data = json.load(json_file)
#         # removing the booked slot from the json file
#         data.get(provider_id).get(date).remove(requested_slot)
#         data.update(data)
#         # updating the json file
#         with open('app/api/providers.json', 'w') as json_file:
#             json.dump(data, json_file, indent=4)
#         return 'Your booking has been confirmed!'