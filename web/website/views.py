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
def manage_employees(): # TODO: Handle CRUD and web (e.x., POST) related requests (i.e., forms)
    # Have other functions within the page to create, update, or delete based on the entires seen above
    if request.method=="POST":
        response = dict(request.form)
        if response["submit"] in ["Update", "Delete"] and response["user_id"]=="": return render_template("home.html") # pop up saying user_id is required for updating or deleting, can re-direct for now to same page with a small error html on top
        if response["submit"] in ["Create"] and response["user_id"]!="": return render_template("home.html") # pop up or same as previous line
        # if nothing failed, meaning the form basic error checks (email format yet to be checked)
        # proceed to process the different requests and input information into the database
        response["org_id"] = ORGANIZATION.id
        # Handling creates
        if response["submit"]=="Create":
            # Check if the required inputs are given (NOT NULL FIELDS)
            # Create the non-dependent table's entires
            # Create the employee table entry
            # Refresh this page with the new information (or use a urlredirect to refresh the page)
            print(response)
            
            ORGANIZATION.create_employee(response)
            """
            {'user_id': '', 'department_id': '1', 'firstname': 'Harri', 
            'lastname': 'Siva', 'username': 'hsiva', 
            'email': 'harrisiva@gmail.com', 'Password': '11@f12', 
            'street_num': '33', 'unit_num': '', 'street_name': 'Street', 
            'city': 'Waterloo', 'province': 'Ontario', 'postal_code': '1N3Z', 
            'country': 'CA', 'institue_num': '12', 'transit_num': '12', 
            'account_num': '323', 'submit': 'Create'}
            """
            pass

    return render_template("organization/manage-employees.html", employees=ORGANIZATION.read_employees())

@views.route("/manage-bank", methods=["GET","POST"])
def manage_bank():

    # Handle bank function from organization manager prespective
    if request.method=="POST":

        # Convert response type, check if response passes basic error handling, add org_id to response
        response = dict(request.form)
        if response["submit"] in ["Update", "Delete"] and response["bank_id"]=="": return render_template("home.html") # pop up saying user_id is required for updating or deleting, can re-direct for now to same page with a small error html on top
        if response["submit"] in ["Create"] and response["bank_id"]!="": return render_template("home.html") # pop up or same as previous line
        response["org_id"]=ORGANIZATION.id

        # If its create, call the required organization function to enter the record into the DB
        if response["submit"]=="Create": ORGANIZATION.create_bank(response)
        if response["submit"]=="Update": ORGANIZATION.update_bank(response) 
        if response["submit"]=="Delete": ORGANIZATION.remove_bank(response)

    return render_template("organization/manage-bank.html", bank_info=ORGANIZATION.view_banks())

@views.route("/manage-addressbook", methods=["GET", "POST"])
def manage_addressbook():
    return render_template("organization/manage-addressbook.html", addressbook=ORGANIZATION.view_addressbook())

# TODO: Second phase of the project. Consists of the view 
@views.route("/employee-dashboard")
def employee():
    # Dashboard for the employee, esentially the employee langing page/view
    # Show data about employee, Show data about the payroll, Show data about performance (restricted for the current employee only)
    # Has redirect to page with limited/restricted CRUD features
    return