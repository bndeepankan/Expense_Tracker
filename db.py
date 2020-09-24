from pymongo import MongoClient


def get_db():

    # client = MongoClient('127.0.0.1', port=27017)
    client = MongoClient("mongodb+srv://bndeepankan:bndeepankan5@dp.gm6xc.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client['expenses_app']['expenses']

    return db

def auth_db():

    # client = MongoClient('localhost', port=27017)
    client = MongoClient("mongodb+srv://bndeepankan:bndeepankan5@dp.gm6xc.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client['expenses_app']['auth']

    return db
