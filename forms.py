from flask_wtf import FlaskForm
from wtforms import Form, StringField

class Expenseform(FlaskForm):
    
    date = StringField('Date')
    value = StringField('Value')
    item = StringField('Item')    
