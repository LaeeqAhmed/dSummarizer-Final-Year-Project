from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask_restful import Api
from flask_restful import Resource
from pandas import read_csv
from json import dump
from json import load
from hashlib import md5
from Email import Email
from pymongo import MongoClient

from flask_cors import CORS, cross_origin

# import error handling file from where you have defined it
# connection string = "mongodb://adminuser:admin1234@cluster0.d35fh.mongodb.net/dSummarizerDB?retryWrites=true&w=majority"

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
api = Api(app)


class Names(Resource):
    def get(self):
        print(request.headers.get("Header-shahram"))  # done
        print(request.args.get("querystring-shahram"))  # done
        with open("names.json", "r") as read_file:
            response = load(read_file); print(response)
        return response


class AddUser(Resource):
    def __init__(self):
        self.connectionString = "localhost:27017"
        self.myclient = MongoClient(self.connectionString)
        self.dataBase = self.myclient["dSummarizerDB"]
        self.collection = self.dataBase["apiusersCollection"]

    def get(self):
        pass

    def post(self):
        username = request.headers.get("username")
        email = request.headers.get("email")

        key = md5(username.encode() + email.encode())
        key = key.hexdigest()
        # insert username email key into database
        print(username)
        print(email)
        mydict = {
            "confirmed": "False",
            "Email": email,
            "username": username,
            "key": key
        }
        self.collection.insert_one(mydict)
        # email the key and varification link to the user
        E = Email(email,username,key)

    def put(self):
        pass

    def delete(self):
        pass


class ConfirmEMail(Resource):
    def __init__(self):
        self.connectionString = "localhost:27017"
        self.myclient = MongoClient(self.connectionString)
        self.dataBase = self.myclient["dSummarizerDB"]
        self.collection = self.dataBase["apiusersCollection"]

    def post(self):
        email = request.form.get("email")
        key = request.form.get("key")
        row = self.collection.find_one({"Email": email})
        for _key in row:
            if row[_key] == key:
                myquery = {"Email": email}
                newvalues = {"$set": {"confirmed": "True"}}
                self.collection.update_one(myquery, newvalues)
                #return render_template("db.html")

class GetPolarity(Resource):
    def get(self):
        name = request.headers.get("name")
        connectionString = "localhost:27017"
        myclient = MongoClient(connectionString)
        dataBase = myclient["dSummarizerDB"]
        collection = dataBase["polarityCollection"]
        row = collection.find_one({"Name": name})
        response = dict()
        for dictKey in row:
            if dictKey != '_id':
                response[dictKey] = row[dictKey]
        return jsonify(response)

class GetExtractiveSummary(Resource):
    def get(self):
        name = request.headers.get("name")
        connectionString = "localhost:27017"
        myclient = MongoClient(connectionString)
        dataBase = myclient["dSummarizerDB"]
        collection = dataBase["extractiveSummaryCollection"]
        row = collection.find_one({"Name": name})
        response = dict()
        for dictKey in row:
            if dictKey != '_id':
                response[dictKey] = row[dictKey]
        return jsonify(response)

class GetAbstractiveSummary(Resource):
    def get(self):
        name = request.headers.get("name")
        connectionString = "localhost:27017"
        myclient = MongoClient(connectionString)
        dataBase = myclient["dSummarizerDB"]
        collection = dataBase["abstractiveSummaryCollection"]
        row = collection.find_one({"Name": name})
        print(row)
        response = dict()
        for dictKey in row:
            if dictKey != '_id':
                response[dictKey] = row[dictKey]
        return jsonify(response)

api.add_resource(Names, "/api/names")
api.add_resource(AddUser, "/api/addUser")
api.add_resource(ConfirmEMail, "/api/signup/confirmation")
api.add_resource(GetPolarity, '/api/dev/get/polarity')
api.add_resource(GetExtractiveSummary, "/api/extractiveSummary")
api.add_resource(GetAbstractiveSummary, "/api/abstractiveSummary")
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
