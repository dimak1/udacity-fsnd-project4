from flask import Flask, render_template, jsonify
from sqlalchemy import *
from setup_database import Base, User, Type
from sqlalchemy.orm import sessionmaker
import requests
import json
import random

engine = create_engine('sqlite:///users.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Clear the tables
# User.__table__.drop()
# Type.__table__.drop()
session.query(User).delete()
session.query(Type).delete()

# Configure random user API
url = "https://randomuser.me/api/"
location = "ca,us"
exclude_params = "login,cell,id"
quantity = "15"

# Call randomuser api to get list of random users in json format
# Sample reposonse at the end of this file
response = requests.get(url + "?noinfo" + "&nat=" + location +
                        "&exc=" + exclude_params + "&results=" + quantity)
# response = requests.get(
# "http://randomuser.me/api/?nat=ca,us&noinfo&exc=login,cell,id&results=2")

json_obj = response.json()

user_types_file = open("user_types.txt", "r")
types = user_types_file.read().split(',')
types_num = len(types)
print(types_num)
user_types_file.close

for t in types:
    print(t)
    user_type = Type(t)
    session.add(user_type)

session.commit()

for item in json_obj["results"]:

    user = User(item["name"]["first"],
                item["name"]["last"],
                item["email"],
                item["gender"][0].upper(),
                item["dob"].split(" ", 1)[0],  # trim to keep date only
                item["phone"],
                item["location"]["street"],
                item["location"]["city"],
                item["location"]["state"],
                item["nat"],
                item["location"]["postcode"],
                item["registered"].split(" ", 1)[0],  # trim to keep date only
                random.randint(1, types_num),
                item["picture"]["large"])
    session.add(user)

session.commit()

print("Added " + quantity + " users")


# Sample output from randomuser api
# {
#     "results": [
#         {
#             "gender": "male",
#             "name": {
#                 "title": "mr",
#                 "first": "clinton",
#                 "last": "johnson"
#             },
#             "location": {
#                 "street": "6216 hillcrest rd",
#                 "city": "garland",
#                 "state": "texas",
#                 "postcode": 33919
#             },
#             "email": "clinton.johnson@example.com",
#             "dob": "1956-05-01 02:46:51",
#             "registered": "2012-10-09 15:57:43",
#             "phone": "(091)-076-3259",
#             "picture": {
#                 "large":
#                   "https://randomuser.me/api/portraits/men/44.jpg",
#                 "medium":
#                    "https://randomuser.me/api/portraits/med/men/44.jpg",
#                 "thumbnail":
#                   "https://randomuser.me/api/portraits/thumb/men/44.jpg"
#             },
#             "nat": "US"
#         }
#     ]
# }
