from flask import Blueprint, render_template, request
from .models import Organization
from copy import deepcopy # (FOR PROTOYPE USE ONLY, ISSUE NEEDS TO BE RESOLVED)
#TODO: Add CSRF token to forms

views = Blueprint('views', __name__)
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

@views.route("/manage-employees", methods=["GET","POST"]) 
def manage_employees(): 
    # Handle employee functions from a db manager prespective
    if request.method=="POST":

        # Convert response type, check if response passes basic error handling, add org_id to response
        response = dict(request.form)
        if response["submit"] in ["Update", "Delete"] and response["user_id"]=="": return render_template("home.html") # pop up saying user_id is required for updating or deleting, can re-direct for now to same page with a small error html on top
        if response["submit"] in ["Create"] and response["user_id"]!="": return render_template("home.html") # pop up or same as previous line
        response["org_id"]=ORGANIZATION.id

        # Call the required organization function to handle the record
        if response["submit"]=="Create": ORGANIZATION.create_employee(response)
        if response["submit"]=="Update": ORGANIZATION.update_employee(response) 
        if response["submit"]=="Delete": ORGANIZATION.view_employees(response)


    return render_template("organization/manage-employees.html", employees=ORGANIZATION.view_employees())

@views.route("/manage-bank", methods=["GET","POST"])
def manage_bank():

    # Handle bank function from organization manager prespective
    if request.method=="POST":

        # Convert response type, check if response passes basic error handling, add org_id to response
        response = dict(request.form)
        if response["submit"] in ["Update", "Delete"] and response["bank_id"]=="": return render_template("home.html") # pop up saying user_id is required for updating or deleting, can re-direct for now to same page with a small error html on top
        if response["submit"] in ["Create"] and response["bank_id"]!="": return render_template("home.html") # pop up or same as previous line
        response["org_id"]=ORGANIZATION.id

        # Call the required organization function to handle the record
        if response["submit"]=="Create": ORGANIZATION.create_bank(response)
        if response["submit"]=="Update": ORGANIZATION.update_bank(response) 
        if response["submit"]=="Delete": ORGANIZATION.remove_bank(response)

    return render_template("organization/manage-bank.html", bank_info=ORGANIZATION.view_banks())

@views.route("/manage-addressbook", methods=["GET", "POST"])
def manage_addressbook():
    
    # Handle addressbook functions from organization manager prespective
    if request.method=="POST":

        # Convert response type, check if response passes basic error handling
        response = dict(request.form)
        if response["submit"] in ["Update", "Delete"] and response["ad_id"]=="": return render_template("home.html") # pop up saying user_id is required for updating or deleting, can re-direct for now to same page with a small error html on top
        if response["submit"] in ["Create"] and response["ad_id"]!="": return render_template("home.html") # pop up or same as previous line

        # Call the required organization function to handle the record
        if response["submit"]=="Create": ORGANIZATION.create_address(deepcopy(response))
        if response["submit"]=="Update": ORGANIZATION.update_address(deepcopy(response)) 
        if response["submit"]=="Delete": ORGANIZATION.remove_address(deepcopy(response))


    return render_template("organization/manage-addressbook.html", addressbook=ORGANIZATION.view_addressbook())

# TODO: Second phase of the project. Consists of the view 
@views.route("/employee-dashboard")
def employee():
    # Dashboard for the employee, esentially the employee langing page/view
    # Show data about employee, Show data about the payroll, Show data about performance (restricted for the current employee only)
    # Has redirect to page with limited/restricted CRUD features
    return