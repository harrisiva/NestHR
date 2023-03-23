from flask import Blueprint, render_template
from .models import database

# Create a blueprint and give the blueprint a name
views = Blueprint('views', __name__) # Way to seperate app out (layout of URLs)

@views.route('/') # Main page (landing page to create a )
def home():
    # Get view tables data and load into the template using the jinja syntax a list
    db_handler = database()
    data = db_handler.viewTables(output=True)
    print(type(data))
    print(data)
    print(type(data[0])) 
    return render_template('base.html', data=data)