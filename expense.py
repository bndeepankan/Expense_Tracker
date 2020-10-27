from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from auth import login_required
from db import get_db
from table import Results, readResults, deleteResult
from forms import Expenseform
from collections import defaultdict
from bson import ObjectId
from spark_sql import sqlOperation

bp = Blueprint('expense', __name__)

@bp.route('/select_expense/', methods=['GET', 'POST'])
@login_required
def select_operation():
    """
    Select the type of CURD operation to be performed
    """
    if request.method == 'POST':
        option = request.form.get("mycheckbox")

        if option == "create":
            return redirect(url_for('expense.create_expense'))
        elif option == "update":
            return redirect(url_for('expense.update_expense'))
        elif option == "read":
            return redirect(url_for('expense.read_expense'))
        elif option == "delete":
            return redirect(url_for('expense.delete_expense'))
        elif option == "sql":
            return redirect(url_for('expense.query_expense'))
        else:
            flash("select checkbox")
    
    return render_template('expense/select.html')


@bp.route('/create_expense/', methods=['GET', 'POST'])
@login_required
def create_expense():
    """
    Adds the expense into the database
    """
    if request.method == 'POST':
        date = request.form["date"]
        value = request.form["value"]
        item = request.form["item"]

        error = None

        if not date:
            error = "Date is required"
        elif not value:
            error = "Value is required"
        elif not item:
            error = "item is required"
        if error is None:
            get_db().insert_one({"user_id": session['user_id'], "date": date, "value": value, "item": item.lower()})
            flash("The item has been added into the record")
            return redirect(url_for('expense.select_operation'))
        else:
            flash(error)

    return render_template('expense/create.html')


@bp.route('/update_expense/', methods=['GET','POST'])
@login_required
def update_expense():
    """
    Shows the list of expense by the current user in the database for update.
    """
    db = get_db()

    if request.method == 'POST':
        date = request.form["date"]
        value = request.form["value"]
        item = request.form["item"]

        query = defaultdict()
        query["user_id"] = session['user_id']

        if date:
            query["date"] = date
        elif value:
            query["value"] = value
        elif item:
            query["item"] = item

        try:
            expenses = db.find(query)
        except:
            flash("There is no data added by the user")
            return redirect(url_for('expense.select_operation'))

        results = list(expenses)
        if not results:
            flash("There is no data added by the user")
            return redirect(url_for('expense.select_operation'))
        else:
            table = Results(results)
            table.border = True
            return render_template('expense/table.html', table = table)
    
    return render_template('expense/update.html')
    

@bp.route('/edit_expense/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    """
    Edit the expense in the database
    """
    db = get_db()
    query = list(db.find({"_id": ObjectId(id)}))[0]
    
    if query:
        form = Expenseform()
        if request.method == "GET":
            form.date.data = query["date"]
            form.value.data = query["value"]
            form.item.data = query["item"]
    else:
        flash("Sorry your data cannot be changed!!!")
        return redirect(url_for('expense.select_operation'))
    if request.method == "POST":
        get_db().find_one_and_update({"_id": ObjectId(id)}, {'$set': {'date': request.form["date"], 'value': request.form["value"], 'item': request.form["item"].lower()}})
        flash("Data is successfully updated")
        return redirect(url_for('expense.select_operation'))
    return render_template('expense/edit.html', form=form)


@bp.route('/read_expense', methods=['GET', 'POST'])
@login_required
def read_expense():
    """
    Reads the transactions stored in the database
    """

    db = get_db()

    if request.method == "POST":
        date = request.form["date"]
        item = request.form["item"]

        query = defaultdict()

        query['user_id'] = session['user_id']

        if date:
            query['date'] = date
        elif item:
            query['item'] = item.lower()
        
        try:
            results = db.find(query)
        except:
            flash("No record of the user")
            return redirect(url_for('expense.select_operation'))

        if not results:
            flash("There is no data added by the user")
            return redirect(url_for('expense.select_operation'))
        else:
            table = readResults(results)
            table.border = True
            return render_template('expense/table.html', table = table)
        
    return render_template('expense/read.html')


@bp.route('/delete_expense', methods=['GET', 'POST'])
@login_required
def delete_expense():

    """
    Delete the expense from the records
    """

    db = get_db()

    if request.method == "POST":
        date = request.form["date"]
        item = request.form["item"]

        query = defaultdict()

        query['user_id'] = session['user_id']

        if date:
            query['date'] = date
        elif item:
            query['item'] = item.lower()
        
        try:
            results = db.find(query)
        except:
            flash("No record of the user")
            return redirect(url_for('expense.select_operation'))

        if not results:
            flash("There is no data added by the user")
            return redirect(url_for('expense.select_operation'))
        else:
            table = deleteResult(results)
            table.border = True
            return render_template('expense/table.html', table = table)
        
    return render_template('expense/delete.html')

@bp.route('/remove_expense/<string:id>', methods=["GET", "POST"])
@login_required
def remove_expense(id):
    """
    Confirmation from the user for deleting the record
    """

    db = get_db()
    query = list(db.find({"_id": ObjectId(id)}))[0]

    if query:
        if request.method == 'POST':
            option = request.form.get("mycheckbox")

            if option == "yes":
                db.remove({"_id": ObjectId(id)})
                flash("Data is successfully deleted!!!")
                return redirect(url_for('expense.select_operation'))
            elif option == "no":
                flash("Data not deleted")
                return redirect(url_for('expense.select_operation'))
            else:
                flash("select one option")
    else:
        flash("Sorry your data cannot be deleted !!!")
        return redirect(url_for('expense.select_operation'))         

    return render_template('expense/remove.html')

@bp.route('/query_expense/', methods=['GET', 'POST'])
@login_required
def query_expense():
    """
    User writes sql query to search on the database
    """

    if request.method == 'POST':
        sql = request.form["sql"]

        error = None

        if not sql:
            error = "query is required"

        if error is None:
            obj = sqlOperation()
            results = obj.searchQuery(sql, session['user_id'])
            table = readResults(results)
            table.border = True
            return render_template('expense/table.html', table = table)
        else:
            flash(error)

    return render_template('expense/sql.html')
