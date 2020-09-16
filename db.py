from pymongo import MongoClient


def get_db():

    client = MongoClient('127.0.0.1', port=27017)
    db = client['expenses_app']['expenses']

    return db
