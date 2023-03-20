use nesthr;

INSERT INTO addressbook(street_num,unit_num,street_name,city,province,postal_code,country)
VALUES(12, 3, 'King Street', 'Waterloo', 'Ontario', 'N1Z3M', 'CA');

INSERT INTO organizations(org_reg,org_name,org_networth,ad_id, org_desc)
VALUES('NZA323DN4X', 'TheDrink', 1000000.50, 1, 'Recreation and nightlife.');

INSERT INTO department(org_id,dep_name,dep_desc,dep_budget,manager_id)
VALUES(1, 'Security', 'Faciliating security and managing bouncing.', 50000.00, NULL);

INSERT INTO project_performance(perf_type_name,perf_type_desc) 
VALUES ('Completed', 'Status provided when a assigned objective is completed. Objectives can be created as seperate entities whose functional structure can be based on a proven performance management and SE workflow model');

INSERT INTO project(org_id,prj_name,prj_desc,perf_type_id,prj_perf_goal) 
VALUES (1,'Training','Provide extra training to security. Can associate with the departments.',1, 50);

INSERT INTO bank(org_id,institute_num,transit_num,account_num) 
VALUES (1,101,352,324553123);

INSERT INTO payroll(org_id,wage,cycle) 
VALUES (1,1000,30); # 1k to be paid every 30 days

INSERT INTO employee(org_id,dep_id,firstname,lastname,username,email,phone,pass,ad_id,bank_id,pay_id) 
VALUES (1,1,'Vasily','Lomachenko','vloma','vloma@pubonking.com',226124356,'a1#xf',1,1,1);

INSERT INTO appraisal(date_achieved,org_id,prj_id,appraised_id,prj_perf_achieved) 
VALUES ('2023-02-25',1,1,1,50);

INSERT INTO transactions(org_id,emp_id,bank_id,wage,EI,vacation,bonus,overtime,net) 
VALUES (1,1,1,50000,0,0,500,0,50500);