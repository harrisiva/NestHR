# Numbers at the end represent the number of inputs
insert_into_bank_4 = "INSERT INTO bank(org_id,institute_num,transit_num,account_num) VALUES (%s,%s,%s,%s);"
insert_into_address_7 = "INSERT INTO addressbook(street_num,unit_num,street_name,city,province,postal_code,country) VALUES(%s, %s, %s, %s, %s, %s, %s);"
insert_into_employee_12 = "INSERT INTO employee(org_id,dep_id,access,firstname,lastname,username,email,phone,pass,ad_id,bank_id,pay_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
insert_into_department_5 = "INSERT INTO department(org_id,dep_name,dep_desc,dep_budget,manager_id)VALUES(%s, %s, %s, %s, %s);"
insert_into_payroll_3 = "INSERT INTO payroll(org_id,wage,cycle)VALUES (%s,%s,%s);"
insert_into_appraisal_5 = "INSERT INTO appraisal(date_achieved,org_id,prj_id,appraised_id,prj_perf_achieved) VALUES (%s, %s, %s, %s, %s);"