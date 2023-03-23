import mysql.connector # Using MySQL Connector rather than SQLAlchemy
from . import private

# From the previous assignments code (author: harrisiva)

# General Database Handler (custom mysql connector wrapper) 
class database:
    def __init__(self): # Load from the private file (TODO: Switch to ENV variables)
        self.host, self.username, self.name = private.HOST, 'admin', 'nesthr'
        self.database = mysql.connector.connect( # Establish a connection with the DB
            host=self.host,
            user=self.username,
            password=private.PASSWORD,
            database=self.name
        )
        self.cursor = self.database.cursor()  # Create a cursor (thorugh which SQL commands are sent)
        # TODO: Handle the different the views in here?
        return

    # Given a fetch type query, this function fetches all the rows and either displays or returns them depending on the bool value of 'output' 
    def fetch(self, query, output=False): 
        self.cursor.execute(query)
        rows = self.cursor.fetchall() # Returns a dictionary of the rows
        if not output:
            for row in rows: print(row) # can be used for debugging the views on the terminal before the front end is built
        return rows if output else None
    
    # Insert (and update) given values into db based on given the sql command and return True or False depending on the success
    def insert(self, sql, values:list):
        success = False
        try:
            self.cursor.execute(sql,values)
            self.database.commit()
        except Exception as e: print("Failed to insert:", e) 
        else: success = True
        return success

    def delete(self,sql):
        success = False
        try: 
            self.cursor.execute(sql)
            self.database.commit()
        except Exception as e: print(e)
        else: success=True
        return success

    def viewTables(self, output=False): return self.fetch("SHOW TABLES;", output)

    def viewEntries(self,table:str,output=False):
        return self.fetch(f'SELECT * FROM {self.name}.{table};',output=output)

    def exit(self):
        self.cursor.close()
        self.database.close()
        return

class Organization():
    def __init__(self): # Uses DB to load organization object's information
        # has a database handler instance on its own
        self.database = database()
        # id, name, and other basic stuff pulled from the ID
        return
    
    # Organization CRUD
    def read_organizations(self):
        # view current organization's data (incl. self and more)
        return
    def create_organization(self):
        # overrrides self data (which would be null)
        return    
    def update_organization(self):
        # Updates in DB and seld
        return
    def delete_organization(self):
        # Deletes the current organization object (ensures cascade condition is met)
        return
    
    # Transaction CRUD
    def create_transaction(self):
        return
    def read_transactions(self):
        return
    def update_transaction(self):
        return
    def delete_transaction(self):
        return

    # Employee CRUD (incl. ) (filters using the current organization)
    def create_employee(self):
        return
    def read_employees(self):
        return 
    def update_employee(self): # Update multi games
        return
    def delete_employee(self):
        return
    
    # Department CRUD
    # Project CRUD

    # Employee Performance Management
    # Enter performance appraisal

    # Employee Payroll Managementent
    # Make payment (all=False, id=None)