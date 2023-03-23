import mysql.connector # Using MySQL Connector rather than SQLAlchemy
from . import private

# From the previous assignments code (author: harrisiva)
# TODO: Custom format function on values to get them in the required dict format
# can use other SQL commands to get the right col names and dict size

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
        self.cursor = self.database.cursor()  # Create a cursor (through which SQL commands are sent)
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

# New Addressbook Handler
class AddressBook():
    def __init__(self, db:database):
        self.database = db
        return
    def create_address(self):
        # Uses the DB handlers insert function
        return
    def read_address(self,id): 
        # Given a ID, return the address in a dictionary
        query = f'SELECT * FROM addressbook WHERE ad_id={id}'
        values = self.database.fetch(query, output=True)[0]
        values = {
            "street_num":values[3],
            "unit_num":values[4],
            "street_name":values[5],
            "city":values[6],
            "province":values[7],
            "postal_code":values[8],
            "country":values[9]
        }
        return values
    def update_address(self,id):
        return
    def delete_address(self,id):
        return

# New Organization Handler
class Organization(): # Used predominantly by the organization related views
    def __init__(self, id=None): # Uses DB to load organization object's information
        
        # Has a database handler instance on its own which is passed to the addressbook (can maintain session use)
        self.database = database()
        self.addressbook = AddressBook(self.database)
       
        self.id = id
        # get the set other information from the database
        query = f'SELECT * FROM organizations WHERE org_id={self.id}'
        values = self.database.fetch(query,output=True)[0]
        if len(values)<=0: print("error, organization ID invalid. May have to create a new organization")
        else:
            self.reg:str = str(values[3])
            self.name:str = str(values[4])
            self.balance:float = float(values[5])
            self.ad_id:int = int(values[6])
            self.desc:str = str(values[7])

            # get and set the address as a dictionary
            self.address:dict = self.addressbook.read_address(self.ad_id)
        return
    
    # Organization CRUD
    def read_organizations(self): # TODO: Can also incldue sum of employees, tranasactional balance, and other summary type info
        return {"reg":self.reg,"name":self.name,"balance":self.balance,"address":self.address,"desc":self.desc}
    
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
    
    def read_employees(self): # uses org_id and db handler to view all the employees in the current organization  
        return self.database.fetch(f'SELECT * FROM employee WHERE org_id={self.id};', output=True) 
    
    def update_employee(self): # Update multi games
        return
    def delete_employee(self):
        return
    
    # TODO:
    # Department CRUD
    # Project CRUD

    # Employee Performance Management
    # Enter performance appraisal

    # Employee Payroll Managementent
    # Make payment (all=False, id=None)