import pymongo

def save_content(item):
    client = pymongo.MongoClient(host='localhost',port=27017)
    db = client.test
    collection = db.chat
    result = collection.insert_one(item)



