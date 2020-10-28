# Expense Tracker Application
This is a tracker of expenses made on the daily basis.

## Live Demo is running on Heroku

http://expense-tracker-dp.herokuapp.com/auth/login

## Following operations can be performed on the web app

1. Create a expense on the Mongodb.

2. Update the exsiting expense in the Mongodb.

3. Read the entire transaction history.

4. Delete a expense from the Mongodb.

5. User authorization support is provided.

6. User can write **SQL Query** to search in their transaction which is performed by **SPARK**. (Not available in Demo server)

## Development Server

``` 
export FLASK_APP=Expense_Tracker
export FLASK_ENV=developement
flask run
```

Install all the requirements which is mentioned on the **requirements.txt**.

```
pip install -r requirements.txt
```
