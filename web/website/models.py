import mysql.connector # Using MySQL Connector rather than SQLAlchemy
from . import private, queries
from copy import deepcopy

# Utility Function
def derive(response:dict): 
    return '=%s,'.join(response.keys())+'=%s', list(response.values())

def clean(response:dict):
    response.pop("submit")
    copy = deepcopy(response)
    for i in response:
        if response[i]=="": copy.pop(i)
    return deepcopy(copy)

# From the previous assignments code (author: harrisiva)
# TODO: Custom format function on values to get them in the required dict format
# can use other SQL commands to get the right col names and dict size

# General Database Handler (custom mysql connector wrapper) 
# TODO: Restructure to just take the stuff it needs from a dict instead of using a values list
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
    def read_organization(self): # TODO: Can also incldue sum of employees, tranasactional balance, and other summary type info
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
    def create_employee(self, response:dict):
        # TODO: Error handling (assume all values are correct for now, enforce later)

        # Insert the bank first
        # Insert the Address next
        # Get the bank and address ID (just values again)
        # Insert into the employee table (use values just pulled)
        """
        INSERT INTO bank(org_id,institute_num,transit_num,account_num) 
        VALUES (1,101,352,324553123);
        """
        #self.database.insert(queries.insert_into_bank_4, [response["org_id"],response["institute_num"],
        #                                                  response["transit_num"],response["account_num"]])
        #print("Insereted into bank")
        """
        INSERT INTO addressbook(street_num,unit_num,street_name,city,province,postal_code,country)
        VALUES(12, 3, 'King Street', 'Waterloo', 'Ontario', 'N1Z3M', 'CA');
        """
        #self.database.insert(queries.insert_into_address_7, [response["street_num"],response["unit_num"],
        #                                                     response["street_name"],response["city"],
        #                                                     response["province"],response["postal_code"],
        #                                                     response["country"]])
        print("Insereted into address")
        # Get the two last added id's from bank and addressbook (or grab it based on the parameteres?)
        addressbook = self.database.fetch("SELECT * FROM addressbook", output=True)[:-1]
        print("Fetched addressess")
        print(addressbook)
        print(type(addressbook))
        bank = self.database.fetch("SELECT * FROM bank", output=True)[:-1]
        print("Fetch bank")
        print(type(bank))
        print(bank)
        """
        INSERT INTO employee(org_id,dep_id,access,firstname,lastname,username,email,phone,pass,ad_id,bank_id,pay_id) 
        VALUES (1,1,1,'Vasily','Lomachenko','vloma','vloma@pubonking.com',226124356,'a1#xf',1,1,1);
        """
        """
        {'user_id': '', 'department_id': '1', 'firstname': 'Harri', 
        'lastname': 'Siva', 'username': 'hsiva', 
        'email': 'harrisiva@gmail.com', 'Password': '11@f12', 
        'street_num': '33', 'unit_num': '', 'street_name': 'Street', 
        'city': 'Waterloo', 'province': 'Ontario', 'postal_code': '1N3Z', 
        'country': 'CA', 'institue_num': '12', 'transit_num': '12', 
        'account_num': '323', 'submit': 'Create'}
        """

        #if self.database.insert("INSERT INTO employee(emp_firstName,emp_lastName, emp_address, emp_phone, emp_username,emp_email, emp_password,emp_type,emp_hourlyWage,emp_salary,organization_id,department_id,bank_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", values): print("Created Employee!")

        return
    def read_employees(self): # uses org_id and db handler to view all the employees in the current organization  
        return self.database.fetch(f'SELECT * FROM employee WHERE org_id={self.id};', output=True) 
    def update_employee(self): # Update multi games
        return
    def delete_employee(self):
        return
    
    def view_banks(self):
        return self.database.fetch(f'SELECT * FROM bank WHERE org_id={self.id};', output=True) 

    def create_bank(self, response:dict):
        self.database.insert(queries.insert_into_bank_4, [response["org_id"],response["institute_num"],
                                                          response["transit_num"],response["account_num"]])
        return

    def remove_bank(self,response:dict):
        sql = f'DELETE FROM bank WHERE bank_id={response["bank_id"]}'
        self.database.delete(sql)
        return

    def update_bank(self,response:dict):
        response = clean(response)
        sql_section,values = derive(response)
        sql = f'UPDATE bank SET {sql_section} WHERE bank_id={response["bank_id"]}'
        self.database.insert(sql, values)
        return
