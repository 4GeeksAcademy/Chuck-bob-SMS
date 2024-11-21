"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db
from flask import Flask, request, jsonify
from twilio.rest import Client
from db import Queue
from sms import send_sms


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

#################################################################################
#######################################################
############################




queue = Queue()

########################################
###########################################################
#################################################################################

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#######################################################################################
###############################################################
#####################################

@app.route('/next', methods=['GET'])                        
def handle_next():
    contact = queue.dequeue()   
    if contact:         
        return jsonify(f"{contact} is up next"), 200  # Return the response
    return jsonify("Error: no one in list"), 404 



@app.route('/all', methods=['GET'])
def get_queue():
    return jsonify(queue.get_queue())


@app.route('/new', methods=['POST'])
def add_to_queue():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    send_sms(data['phone'], "you have successfully joined the queue")
    queue.enqueue(data)
    return jsonify(f"message: Person added successfully, contact: {data['phone']}" ), 201



#######################################
###############################################################
########################################################################################

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
