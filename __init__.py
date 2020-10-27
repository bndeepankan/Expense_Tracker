"""
This app implements a money tracking tool and exposes a RESTful API meant to be used by a frontend
"""
import os
from flask import Flask, redirect, url_for
from db import get_db

app = Flask(__name__, instance_relative_config=True)

app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'Expense_Tracker.mongo')
)  

@app.route('/')
def index():
    return "Hello World!!!"

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from . import auth
app.register_blueprint(auth.bp)

from .import expense
app.register_blueprint(expense.bp)

app.add_url_rule('/select_expense', endpoint='select_operation')

if __name__ == '__main__':
    app.run(debug=True)
