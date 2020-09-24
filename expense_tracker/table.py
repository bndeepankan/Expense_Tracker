from flask_table import Table, Col, LinkCol

class Results(Table):

    obj_id = Col('_id', show=False)
    user_id = Col('user_id', show=False)
    date = Col('Date')
    value = Col('Value')
    item = Col('Item')
    edit = LinkCol('Edit', 'expense.edit_expense', url_kwargs=dict(id='_id'))

class readResults(Table):

    obj_id = Col('_id', show=False)
    user_id = Col('user_id', show=False)
    date = Col('Date')
    value = Col('Value')
    item = Col('Item')

class deleteResult(Table):

    obj_id = Col('_id', show=False)
    user_id = Col('user_id', show=False)
    date = Col('Date')
    value = Col('Value')
    item = Col('Item')
    delete = LinkCol('Delete', 'expense.remove_expense', url_kwargs=dict(id='_id'))