
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import bcrypt
app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')
db = client.SentencesDatabase
users = db['Users']

class Register(Resource):
    def post(self):
        #Step 1 is tp get posted data
        postedData = request.get_json()
        
        # Get the data
        username = postedData["username"]
        password = postedData["password"]
        # hash(password + salt) = uhuhgruygh
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        
        # Store username and pw into the database
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Sentence": "",
            "Tokens": 6
        })

        retJson = {
            "status": 200,
            "msg": "You successfuly signed up"
        }
        return jsonify(retJson)
def verifyPw(username, password):
    hashed_pw = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False
def countTokens(username):
    tokens = users.find({
        "Username": username
    })[0]["Tokens"]

    return tokens


class Store(Resource):
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]
        
        correct_pw = verifyPw(username, password)
        if not correct_pw:
            retjson = {
                "status": 302
            }
            return jsonify(retjson)
        
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                "status": 301
            }
            return jsonify(retJson)

        users.update({
            "Username": username
            }, {
                "$set": {
                    "Sentence": sentence,
                    "Tokens": num_tokens -1

              }
            })
        
        return {"message": "sentence sent successfuly"}, 200

class Get(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        correct_pw = verifyPw(username, password)
        if not correct_pw:
            retjson = {
                "status": 302
            }
            return jsonify(retjson)

        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                "status": 301
            }
            return jsonify(retJson)
            
        users.update({
            "Username": username
            }, {
                "$set": {
                    "Sentence": sentence,
                    "Tokens": num_tokens -1

              }
            })
        
        sentence = users.find({
            "Username": username
        })[0]["Sentence"]

        retJson = {
            "status": 200,
            "sentence": sentence
        }
        return jsonify(retJson)


api.add_resource(Register, "/register")
api.add_resource(Store, "/store")
api.add_resource(Get, "/get")

if __name__ == '__main__':
    app.run(host='0.0.0.0')

"""
from pymongo import MongoClient
from flask import Flask
from flask_restful import Api, Resource
app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')
db = client.aNewDB
UserNum = db['UserNum']

UserNum.insert({
    'num_of_users': 0
})


class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1
        UserNum.update({}, {"$set": {"num_of_users": new_num}})
        return str("Hello user ") + str(new_num)

api.add_resource(Visit, "/visit")
@app.route('/hello')
def index():
    return {"message": "Hello Universe!"}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
"""
