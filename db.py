from pymongo import MongoClient


class mongoURI():

    def __init__(self):
        self.expense_uri = "mongodb+srv://bndeepankan:bndeepankan5@dp.gm6xc.gcp.mongodb.net/expenses_app.expenses?retryWrites=true&w=majority"
        self.auth_uri = "mongodb+srv://bndeepankan:bndeepankan5@dp.gm6xc.gcp.mongodb.net/expenses_app.auth?retryWrites=true&w=majority"

def get_db():

    # client = MongoClient('127.0.0.1', port=27017)
    obj = mongoURI()
    client = MongoClient(obj.expense_uri)
    db = client['expenses_app']['expenses']

    return db

def auth_db():

    # client = MongoClient('localhost', port=27017)
    obj = mongoURI()
    client = MongoClient(obj.auth_uri)
    db = client['expenses_app']['auth']

    return db
