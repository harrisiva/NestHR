from flask import Blueprint, render_template
from .models import database

# Create a blueprint and give the blueprint a name
views = Blueprint('views', __name__) # Way to seperate app out (layout of URLs)

@views.route('/') # Main page (landing page to create a )
def home():
    # Required features:
        # Create organization
        # Login to existing organization
        # Sign up

    db_handler = database()  #Handler created for each sessionßß
    data = db_handler.viewTables(output=True)
    print(type(data))
    print(data)
    print(type(data[0])) 
    return render_template('base.html', data=data)

@views.route('/organization-dashboard')
def organization(): # Restricted to any particular organization based on the session ID?
    # Dashboard for the organization, esentially the organization landing page/view
    # Show data from special queries
    # Show buttons to go to crud features
    # Show organizations basic details (access level based) (SELECT where ORG name matches)
    # Has redirect to page with CRUD features
    
    # Initiate database handler
    
    return 

@views.route("/employee-dashboard")
def employee():
    # Dashboard for the employee, esentially the employee langing page/view
    # Show data about employee
    # Show data about the payroll
    # Show data about performance (restricted for the current employee only)
    # Has redirect to page with CRUD features
    
    # 
    
    return