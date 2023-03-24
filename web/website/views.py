from flask import Blueprint, render_template
from .models import Organization

# Create a blueprint and give the blueprint a name
views = Blueprint('views', __name__) # Way to seperate app out (layout of URLs)
ORGANIZATION = Organization(1) # Means it only works for one session at a time currently (so one DB admin DBMS view accesses per connection)

@views.route('/') # Main page (landing page to create a )
def home():
    # Need to use the global variable on ORGANIZATON to modify it
    # Required features:
        # Create organization
        # Login to existing organization
        # Sign up

    # Create a global database variable and have access variable in the input so the access handling is done in both the models and the views but the models would not need to be modified more

    # get the required data and append it into the data list in its most attomic format
    # required data:
        # general organization details
        # special queries data
    return render_template('home.html')

@views.route('/organization-dashboard')
def organization(): # Restricted to any particular organization based on the session ID?
    # Dashboard for the organization, esentially the organization landing page/view
    # Import basic organization data and special query data, can be passed inline (but might be bad practice)
    return render_template("organization.html", profile=ORGANIZATION.read_organization())

@views.route("/manage-employees")
def manage_employees():
    return render_template("manage-employees.html", employees=ORGANIZATION.read_employees())

@views.route("/employee-dashboard")
def employee():
    # Dashboard for the employee, esentially the employee langing page/view
    # Show data about employee
    # Show data about the payroll
    # Show data about performance (restricted for the current employee only)
    # Has redirect to page with CRUD features
    return