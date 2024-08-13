# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt


import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    employee_information = get_employee_information(filters)

    if not employee_information:
        frappe.msgprint('No records found')
        return columns, employee_information

    for d in employee_information:
        row = frappe._dict({
            'transfer_date': d.transfer_date,
            'employee1': d.employee1,
            'employee': d.employee,
			'division': d.division,
            'from_branch': d.from_branch,
            'department': d.department,
            'designation': d.designation,
            'to_branch': d.to_branch,
         	'department1': d.department1,
            'designation1': d.designation1,
			'role': d.role,
            'role1': d.role1,
			
        })
        data.append(row)

    return columns, data

def get_columns():
    return [
        {
            'fieldname': 'transfer_date',
            'label': "Transfer Date",
            'fieldtype': 'date',
            'width': '120'
        },
        {
            'fieldname': 'employee1',
            'label': "Req. ID",
            'fieldtype': 'link',
            'width': '120'
        },
        {
            'fieldname': 'employee',
            'label': "Employee Name",
            'fieldtype': 'Data',
            'width': '180'
        },
        {
            'fieldname': 'from_branch',
            'label': "From Branch",
            'fieldtype': 'Data',
            'width': '120'
        },
      		{
            'fieldname': 'to_branch',
            'label': "To Branch",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'department',
            'label': "From Department",
            'fieldtype': 'Data',
            'width': '120'
        },
      		{
            'fieldname': 'department1',
            'label': "To Department",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'designation',
            'label': "From Position",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'designation1',
            'label': "To Position",
            'fieldtype': 'Data',
            'width': '120'
        },
		  {
            'fieldname': 'role',
            'label': "From Roel",
            'fieldtype': 'Data',
            'width': '120'
        },
    		  {
            'fieldname': 'role1',
            'label': "To Role",
            'fieldtype': 'Data',
            'width': '120'
        },
    
        
    ]

def get_employee_information(filters):
		return frappe.db.sql(
			f"""SELECT *
			FROM `tabEmployee Transfer`""",
			as_dict=1,
		)
