from flask import Blueprint, render_template

# Create a blueprint and give the blueprint a name
views = Blueprint('views', __name__) # Way to seperate app out (layout of URLs)

@views.route('/') # Main page
def home():
    # Getting data here as dictonaries and giving inputs as dictionaries throguh and to the custom functions we built in models (use wraper code)
    return render_template('base.html')