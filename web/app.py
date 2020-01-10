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
