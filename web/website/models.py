import mysql.connector # Using MySQL Connector (and custom db wrapper) rather than SQLAlchemy
from . import private, queries
from copy import deepcopy
# TODO: CRUD Functions Error handling (assume all values are correct for now, enforce later)

# Utility Function
def derive(response:dict): 
    return '=%s,'.join(response.keys())+'=%s', list(response.values())

def clean(response:dict):
    response.pop("submit")
    copy = deepcopy(response)
    for i in response:
        if response[i]=="": copy.pop(i)
    return deepcopy(copy)

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

class Organization(): 
    def __init__(self, id=None): 
        
        # Has a database handler instance on its own which is passed to the addressbook (can maintain session use)
        self.database = database()       
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
            self.address:dict = self.get_address(self.ad_id)
        return
    
    # Organization CRUD
    def read_organization(self):
        return {"reg":self.reg,"name":self.name,"balance":self.balance,"address":self.address,"desc":self.desc}
 
    # Employee CRUD (incl. ) (filters using the current organization)
    def create_employee(self, response:dict): 
        self.database.insert(queries.insert_into_employee_12, 
                             [response['org_id'],response['dep_id'],response['access'],
                              response['firstname'],response['lastname'],response['username'],
                              response['email'],response['phone'],response['pass'],
                              response['ad_id'],response['bank_id'],response['pay_id']])
        return
     
    def view_employees(self):
        return self.database.fetch(f'SELECT * FROM employee WHERE org_id={self.id};', output=True) 
    
    def update_employee(self, response): 
        response = clean(response)
        sql_section,values = derive(response)
        sql = f'UPDATE employee SET {sql_section} WHERE emp_id={response["emp_id"]} and org_id={self.id}'
        self.database.insert(sql, values)
        return

    def remove_employee(self, response):
        sql = f'DELETE FROM employee WHERE emp_id={response["emp_id"]}'
        self.database.delete(sql)
        return
    
    def view_addressbook(self): 
        return self.database.fetch("SELECT * FROM addressbook", output=True)

    def get_address(self,id): 
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

    def create_address(self, response):
        self.database.insert(queries.insert_into_address_7, [response["street_num"],response["unit_num"],
                                                             response["street_name"],response["city"],
                                                             response["province"],response["postal_code"],
                                                             response["country"]])
        return
    
    def remove_address(self,response):
        sql = f'DELETE FROM addressbook WHERE ad_id={response["ad_id"]}'
        self.database.delete(sql)
        return

    def update_address(self,response):
        response = clean(response)
        sql_section,values = derive(response)
        sql = f'UPDATE addressbook SET {sql_section} WHERE ad_id={response["ad_id"]}'
        self.database.insert(sql, values)
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
