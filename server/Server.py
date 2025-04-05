from flask import Flask
from flask import jsonify
from flask_cors import CORS,cross_origin
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import functions
import config
import os
import dotenv
#load env
dotenv.load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.config["COR_HEADERS"] =  "Content-Type"
app.config['JWT_SECRET_KEY'] = SECRET_KEY
CORS(app)
jwt = JWTManager(app)

#login
@app.route("/login", methods = ["POST"])
@cross_origin(origins= "*")
def login():return functions.login()

@app.route("/getuser", methods = ["GET"])
@cross_origin(origins= "*")
@jwt_required()
def getinfo():return functions.user_info()


if __name__ == "__main__":
    app.run(host= config.HOST, port= config.PORT)



