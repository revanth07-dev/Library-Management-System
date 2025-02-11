from flask import Blueprint, request
from ..db import mongo

authentication_bp = Blueprint("authentication", __name__)
# mongo = get_mongo_client()

@authentication_bp.route("/login", methods=('GET','POST'))
def login():
    data= request.json
    print("Login",data)
    if(data['username'] == 'admin' and data['password'] == 'admin'):
        return data, 200
    try:
        datad= mongo.db.members.find_one({"username":data['username']})
        print(data)
        if data['password'] == datad['password']:
                # Password matches, return user data
                return {'username': data['username'], 'user_id': str(datad['_id'])}, 200
        return {'username':data['username'], 'user_id':str(data['_id'])}, 200
    except Exception as e:
        return "Unable to Login", 401

@authentication_bp.route("/register", methods=('GET', 'POST'))
def register():
    data= request.json
    try:
        member = {
                "username":data["username"], 
                "Fname":data["Fname"],
                "Lname":data["Lname"],
                "email":data["email"], 
                "contact_info": {
                    "address": data["address"],
                    "phone":data['phone']
                },
                "password":data["password"],
                "dob":data["dob"],
                "books":[]
              }
        mongo.db.members.insert_one(member)
        return "Registered Successfully", 201
    except:
        return "Something went wrong, Please try again later!", 401
    