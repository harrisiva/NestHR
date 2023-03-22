from flask import Blueprint, render_template

# Create a blueprint and give the blueprint a name
views = Blueprint('views', __name__) # Way to seperate app out (layout of URLs)

@views.route('/') # Main page
def home():
    return render_template('base.html')