from flask import Blueprint, render_template, request
from .models import Organization
#TODO: Build forms (employee management)
#TODO: Add CSRF token to forms
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

@views.route('/organization-dashboard', methods=["GET","POST"])
def organization(): # Restricted to any particular organization based on the session ID?
    special = None # TODO: Import special SQL query command responses
    # TODO: CUD from CRUD
    # TODO: Page and form for RUDing organization data from the data
    # Pass to a page with a form to CRUD the org info in the database  # Leave blank to skip (for now, can change to select col to change later)
    return render_template("organization/organization.html", profile=ORGANIZATION.read_organization())

@views.route("/manage-employees", methods=["GET","POST"]) # TODO: Form for managing employee
def manage_employees(request): # TODO: Handle CRUD and web (e.x., POST) related requests (i.e., forms)
    # Have other functions within the page to create, update, or delete based on the entires seen above
    if request.post:
        print()
        
    return render_template("organization/manage-employees.html", employees=ORGANIZATION.read_employees())

# TODO: Second phase of the project. Consists of the view 
@views.route("/employee-dashboard")
def employee():
    # Dashboard for the employee, esentially the employee langing page/view
    # Show data about employee, Show data about the payroll, Show data about performance (restricted for the current employee only)
    # Has redirect to page with limited/restricted CRUD features
    return