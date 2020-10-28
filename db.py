from pymongo import MongoClient


class mongoURI():

    def __init__(self):
        self.expense_uri = MongoClient('127.0.0.1', port=27017)
        self.auth_uri = MongoClient('127.0.0.1', port=27017)

def get_db():

    obj = mongoURI()
    client = MongoClient(obj.expense_uri)
    db = client['expenses_app']['expenses']

    return db

def auth_db():

    obj = mongoURI()
    client = MongoClient(obj.auth_uri)
    db = client['expenses_app']['auth']

    return db
