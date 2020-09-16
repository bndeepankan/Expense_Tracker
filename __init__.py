"""
This app implements a money tracking tool and exposes a RESTful API meant to be used by a frontend
"""

from flask import Flask, request, render_template, redirect, url_for, flash
import json
from bson import json_util
from .db import get_db
import requests


def create_app():

    app = Flask(__name__, instance_relative_config=True)

    @app.route('/', methods=['GET', 'POST'])
    def select_operation():
        """
        select the type of CURD operation to be performed.
        """
        if request.method == 'POST':
            option = request.form.get("mycheckbox")
            if option == "create":
                return redirect(url_for('create_expense'))
            elif option == "update":
                return redirect(url_for('update_expense'))
            elif option == "read":
                return redirect(url_for('read_expense'))
            else:
                return redirect(url_for('delete_expense'))
        return render_template('select.html')

    @app.route('/create_expense/', methods=['GET','POST'])
    def create_expense():
        """
        Presents the data to be added into Json object.
        return: Output of the operation
        """
        if request.method == "POST":
            date = request.form["date"]
            value = request.form["value"]
            category = request.form["category"]
            error = None

            if not date:
                error = "Date is required"
            elif not value:
                error = "Value is required"
            elif not category:
                error = "Category is required"
            if error is None:
                expense_json = {"date": date, "value": value, "category": category}
                r = requests.post('http://127.0.0.1:5000/set_expense/', json=expense_json)
                return r.text

            flash(error)

        return render_template('create.html')

    @app.route('/update_expense/', methods=['GET','POST'])
    def update_expense():
        """
        Take the input for which data to be updated.
        return: output of the operation
        """
        if request.method == "POST":
            date = request.form["date"]
            value = request.form["value"]
            category = request.form["category"]
            error = None

            if not date:
                error = "Date is required"
            elif not value:
                error = "Value is required"
            elif not category:
                error = "Category is required"
            if error is None:
                expense_json = {"date": date, "value": value, "category": category}
                r = requests.post('http://127.0.0.1:5000/modify_value_expense/', json=expense_json)
                return r.text

            flash(error)

        return render_template('update.html')

    @app.route('/read_expense/', methods=['GET','POST'])
    def read_expense():
        """
        Displays the data based on the user inputs
        """
        if request.method == "POST":
            opt = request.form.get("mycheckbox")
            if opt == "all":
                return redirect(url_for('list_expenses'))
            else:
                return redirect(url_for('get_expense', date=opt))
        return render_template('read.html')

    @app.route('/delete_expense/', methods=['GET', 'POST'])
    def delete_expense():
        """
        Reads the data which user wants to delete
        """
        if request.method == 'POST':
            date = request.form["date"]
            value = request.form["value"]
            category = request.form["category"]
            error = None

            if not date:
                error = "Date is required"
            elif not value:
                error = "Value is required"
            elif not category:
                error = "Category is required"
            if error is None:
                expense_json = {"date": date, "value": value, "category": category}
                r = requests.post('http://127.0.0.1:5000/remove_expense/', json=expense_json)
                return r.text

            flash(error)

        return render_template('delete.html')

    # curl -d post http://localhost:5000/list_all_expenses/
    @app.route("/list_all_expenses/", methods=["GET"])
    def list_expenses():
        """
        :return: returns a list of all expenses
        """

        db = get_db()
        cursor_expenses = db.find({})
        matches = list(cursor_expenses)
        if len(matches) > 0:
            return json.dumps(matches, default=json_util.default)
        else:
            return "Empty response!!!"

    # curl  http://localhost:5000/get_expense/01012020
    @app.route("/get_expense/<string:date>", methods=["GET"])
    def get_expense(date):
        """
        :param date: a DDMMYYYY date
        :return: returns a list of expenses in the provided date
        """

        db = get_db()
        cursor_expenses = db.find({"date": date})
        matches = list(cursor_expenses)
        if len(matches) > 0:
            return json.dumps(matches, default=json_util.default)
        else:
            return "Empty response!!!"

    # you can query this with curl -d'{"date":"01012020", "value":192.1, "category":"groceries"}'  http://loost:5000/set_expense/
    @app.route("/set_expense/", methods=["POST"])
    def add_expense():
        # adds an expense to mongo from the frontend
        # json is provided in the body of the request
        # {
        #   "date": "DDMMYYYY",
        #   "value": float
        #   "category": string
        # }
        #
        expense_json = request.get_json(force=True)

        db = get_db()
        for key in expense_json:
            if key == "date":
                expense_json[key] = str(expense_json[key])
            elif key == "value":
                expense_json[key] = float(expense_json[key])
            elif key == "category":
                expense_json[key] = str(expense_json[key])
        db.insert_one(expense_json)
        return "done"

    @app.route("/modify_value_expense/", methods=["POST"])
    def update_value():
        """
           finds and update the value of a record on the basis of date and category.
        """

        expense_json = request.get_json(force=True)

        db = get_db()
        for key in expense_json:
            if key == "date":
                expense_json[key] = str(expense_json[key])
            elif key == "value":
                expense_json[key] = float(expense_json[key])
            elif key == "category":
                expense_json[key] = str(expense_json[key])
        db.find_one_and_update({"date": expense_json["date"], "category": expense_json["category"]}, {'$set': {'value': expense_json["value"]}})
        return "done"

    @app.route("/remove_expense/", methods=["POST"])
    def remove_expense():
        """
            finds and remove a expense based on the record.
        """
        expense_json = request.get_json(force=True)

        db = get_db()
        for key in expense_json:
            if key == "date":
                expense_json[key] = str(expense_json[key])
            elif key == "value":
                expense_json[key] = float(expense_json[key])
            elif key == "category":
                expense_json[key] = str(expense_json[key])
        n = len(list(db.find(expense_json)))
        if n > 0:
            db.remove(expense_json)
            return f"deleted {n} such records"
        else:
            return "no such records"
    

    return app
