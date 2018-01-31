from datetime import datetime

import sys
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient(host="localhost", port=27017, username="yfsrobot",
                     password="yfsrobotksdw1212180")

db = client['yfsrobot']

user_id = sys.argv[1]

result = db.collection('phoneplan').find({"owner": user_id, "isdial": 1}).count()

print(result)



