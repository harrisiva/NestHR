from copy import deepcopy
# Small function to update
def derive(values:dict): 
    return '=%s,'.join(values.keys())+'=%s', list(values.values())

response = {'user_id': '', 'department_id': '1', 'firstname': 'Harri', 
        'lastname': 'Siva', 'username': 'hsiva', 
        'email': 'harrisiva@gmail.com', 'Password': '11@f12', 
        'street_num': '33', 'unit_num': '', 'street_name': 'Street', 
        'city': 'Waterloo', 'province': 'Ontario', 'postal_code': '1N3Z', 
        'country': 'CA', 'institue_num': '12', 'transit_num': '12', 
        'account_num': '', 'submit': ''}

# Convert response to two lists 

