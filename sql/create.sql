create database nesthr; # .ca domain is available for the low on godady, can build the whole app as a project, lmk :) 
use nesthr;

CREATE TABLE addressbook ( # Used to atomically keep track of addresses in the system (ensures addresses are 1NF, therefore other tables can be 1NF+)
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    ad_id INT PRIMARY KEY AUTO_INCREMENT, # Primary Key
    
    street_num SMALLINT NOT NULL,
    unit_num SMALLINT,
    street_name TINYTEXT NOT NULL,
    city TINYTEXT NOT NULL,
    province TINYTEXT NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(80) NOT NULL
);

CREATE TABLE organizations ( # 1NF, ..?
	date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    org_id INT PRIMARY KEY AUTO_INCREMENT, # Primary Key
    org_reg VARCHAR(25) UNIQUE NOT NULL, # Candidate Key
    
    org_name TINYTEXT NOT NULL, 
    org_networth DECIMAL(15,2) NOT NULl,
    ad_id INT,
    org_desc TEXT NOT NULL,
	
    FOREIGN KEY (ad_id) REFERENCES addressbook(ad_id) ON DELETE SET NULL # Alert in system if missing
);

CREATE TABLE department( 
	date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	
    org_id INT NOT NULL, 
    dep_id INT PRIMARY KEY AUTO_INCREMENT, 
    
    dep_name VARCHAR(50) UNIQUE NOT NULL,
    dep_desc TEXT NOT NULL,
    dep_budget DECIMAL(15,2) NOT NULL,
    
    FOREIGN KEY (org_id) REFERENCES organizations(org_id) ON DELETE CASCADE # Ensures that the weak entity is removed when the strong entity it depnds on is removed
	# (Note: This table is altered later to add manager_id as an attribute after the employee table is created)
);

CREATE TABLE project_performance(
	date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	
    perf_type_id INT PRIMARY KEY AUTO_INCREMENT,
    
    perf_type_name VARCHAR(20) NOT NULL,
    perf_type_desc TEXT NOT NULL
);

CREATE TABLE project( 
	date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    org_id INT NOT NULL,
    prj_id INT PRIMARY KEY AUTO_INCREMENT,
    
    prj_name VARCHAR(50) NOT NULL,
    prj_desc TEXT NOT NULL,
    perf_type_id INT,
    prj_perf_goal INT NOT NULL CHECK (prj_perf_goal >= 0 AND prj_perf_goal <= 100),  # Performance targets are percents represented as a int from 0 to 100
	
    FOREIGN KEY (org_id) REFERENCES organizations(org_id) ON DELETE CASCADE, # Ensures that the weak entity is removed when the strong entity it depnds on is removed
	FOREIGN KEY (perf_type_id) REFERENCES project_performance(perf_type_id) ON DELETE SET NULL # An alert needs to be raised by the system
);

CREATE TABLE bank (
	date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    org_id INT NOT NULL,
    bank_id INT PRIMARY KEY AUTO_INCREMENT,
    
    institute_num VARCHAR(50) NOT NULL,
    transit_num VARCHAR(50) NOT NULL, 
    account_num VARCHAR(50) NOT NULL UNIQUE, # Candidate key, but ignored for privacy reasons
	
    FOREIGN KEY (org_id) REFERENCES organizations(org_id) ON DELETE CASCADE # Ensures that the weak entity is removed when the strong entity it depnds on is removed
);

CREATE TABLE payroll (
	date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    org_id INT NOT NULL,
    pay_id INT PRIMARY KEY AUTO_INCREMENT,
    
    wage DECIMAL(15,2) NOT NULL,
    cycle INT NOT NULL, # number of days per payment
    prev_pay TIMESTAMP DEFAULT NULL,
    next_pay TIMESTAMP DEFAULT NULL, #TODO: Need to derive it based on prev_pay's timestamp + cycle(days)
    
    FOREIGN KEY (org_id) REFERENCES organizations(org_id) ON DELETE CASCADE
);

CREATE TABLE employee(
	date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	
    org_id INT NOT NULL,
    emp_id INT PRIMARY KEY AUTO_INCREMENT,
    dep_id INT,
    
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE, # (Candidate ignored for privacy reasons) Unique for each user but we can create a user profile to store users application preferences
    email VARCHAR(50) NOT NULL UNIQUE, # (Candidate ignored for privacy reasons)
	phone BIGINT NOT NULL, 
    pass VARCHAR(50) NOT NULL, 
    
	ad_id INT,
    bank_id INT,
    pay_id INT,
    
    FOREIGN KEY (org_id) REFERENCES organizations(org_id) ON DELETE CASCADE,
    FOREIGN KEY (dep_id) REFERENCES department(dep_id) ON DELETE SET NULL,
    FOREIGN KEY (ad_id) REFERENCES addressbook(ad_id) ON DELETE SET NULL,
    FOREIGN KEY (bank_id) REFERENCES bank(bank_id) ON DELETE SET NULL,
    FOREIGN KEY (pay_id) REFERENCES payroll(pay_id) ON DELETE SET NULL
);

# Alter the department table and add the manager_id now since the referenced table (i.e., employee) is created.
ALTER TABLE department ADD manager_id INT DEFAULT NULL;
ALTER TABLE department ADD FOREIGN KEY (manager_id) REFERENCES employee(emp_id) ON DELETE SET NULL;

CREATE TABLE appraisal( 
	date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	
    date_achieved DATE NOT NULL,
    org_id INT NOT NULL,
    prj_id INT,
    appr_id INT PRIMARY KEY AUTO_INCREMENT,
	
	appraiser_id INT,	
    appraised_id INT,
    prj_perf_achieved INT NOT NULL CHECK (prj_perf_achieved >= 0 AND prj_perf_achieved <= 100),

	FOREIGN KEY (org_id) REFERENCES organizations(org_id) ON DELETE CASCADE,
    FOREIGN KEY (prj_id) REFERENCES project(prj_id) ON DELETE SET NULL, 
    FOREIGN KEY (appraiser_id) REFERENCES employee(emp_id) ON DELETE SET NULL,
    FOREIGN KEY (appraised_id) REFERENCES employee(emp_id) ON DELETE SET NULL
);

CREATE TABLE transactions(
	date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    tran_id INT PRIMARY KEY AUTO_INCREMENT,
    org_id INT NOT NULL,
    emp_id INT,
    bank_id INT,
    
    wage DECIMAL(10,2) CHECK (wage>=0),
    EI DECIMAL(10,2) CHECK (EI<=0),
	vacation DECIMAL(10,2) CHECK (vacation<=0),
	bonus DECIMAL(10,2) CHECK (bonus >= 0),    
    overtime DECIMAL(10,2) CHECK (overtime>=0),
    net DECIMAL(10,2) NOT NULL, # Todo: Make derived and update the associated organizations networth

    FOREIGN KEY (org_id) REFERENCES organizations(org_id) ON DELETE CASCADE,
    FOREIGN KEY (emp_id) REFERENCES employee(emp_id) ON DELETE SET NULL,
    FOREIGN KEY (bank_id) REFERENCES bank(bank_id) ON DELETE SET NULL
);