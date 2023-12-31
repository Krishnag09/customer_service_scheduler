from flask import Blueprint
from flask_restful import Api
from .resources import HelloWorld, ServiceScheduler, CheckIn, ServiceSchedulerPro
api_bp = Blueprint('api', __name__, url_prefix='/api') # create a Blueprint object cin reference for entire app
api = Api(api_bp)

api.add_resource(HelloWorld, '/hello')
api.add_resource(ServiceScheduler, '/service')
api.add_resource(CheckIn, '/checkin')
api.add_resource(ServiceSchedulerPro, '/servicepro')

