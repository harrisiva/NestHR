from flask import Blueprint, render_template
from .models import Organization

# Create a blueprint and give the blueprint a name
views = Blueprint('views', __name__) # Way to seperate app out (layout of URLs)

@views.route('/') # Main page (landing page to create a )
def home():
    # Required features:
        # Create organization
        # Login to existing organization
        # Sign up

    organization = Organization(1) # Initialize new organization object
    # get the required data and append it into the data list in its most attomic format
    # required data:
        # general organization details
        # special queries data
    return render_template('base.html')

@views.route('/organization-dashboard')
def organization(): # Restricted to any particular organization based on the session ID?
    # Dashboard for the organization, esentially the organization landing page/view
    # Import basic organization data and special query data
    organization = Organization(1) # Handle using POST requests
    profile = organization.read_organizations()
    employees = organization.read_employees()
    print(profile)
    return render_template("organization.html", profile=profile,employees=employees)

@views.route("/manage-employees")
def manage_employees():
    return render_template("manage-employees.html")

@views.route("/employee-dashboard")
def employee():
    # Dashboard for the employee, esentially the employee langing page/view
    # Show data about employee
    # Show data about the payroll
    # Show data about performance (restricted for the current employee only)
    # Has redirect to page with CRUD features
    return