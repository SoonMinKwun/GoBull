from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from pymongo import message
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
from werkzeug.wrappers import response

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost/Stock_Emo_DB"
mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create_user():
    # Receiving data
    username = request.json['username'] #Sean
    password = request.json['password']
    email = request.json['email']

    if username and password and email:
        hashed_password = generate_password_hash(password)
        id = mongo.db.user.insert(
            {"username" : username, "password" : hashed_password, "email" : email}
        )
        response = {
            "id" : str(id),
            "username" : username,
            "password" : password,
            "email" : email
        }
        return response
    else:
        return not_found()

    return {'message' : 'received'}

@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.user.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.user.find_one({"_id" : ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({"_id" : ObjectId(id)})
    response = jsonify({"message" : "User " + id + " was Deleted successfully."})
    return response

@app.route('/users/<id>', methods=['PATCH'])
def update_user(id):
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]

    if username and password and email:
        hashed_password = generate_password_hash(password)
        mongo.db.user.update_one({"_id" : ObjectId(id)}, {"$set" : {
            "username" : username,
            "password" : hashed_password,
            "email" : email
        }})
        response = jsonify({"message" : "User " + id + " was updated successfully"})
        return response

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        "message" : "Resource Not Found: " + request.url,
        "status" : 404
    })
    response.status_code = 404
    return response

if __name__== "__main__":
    app.run(debug=True)