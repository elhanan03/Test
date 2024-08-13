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
            'refno': d.refno,
            'full_name': d.full_name,
            'status': d.status,
            'date_of_joining': d.date_of_joining,
            'gender': d.gender,
            'basic_salary': d.basic_salary,
            'phone_number': d.phone_number,
            'email': d.email,
            'division': d.division,
            'department': d.department,
            'designation': d.designation,
            'employement_type': d.employement_type,
            'role': d.role,
            'branch': d.branch,
            'birth_date': d.birth_date,
            'sub_city__zone': d.sub_city__zone,
            'woreda': d.woreda,
            'kebele': d.kebele,
            'house_number': d.house_number,
        })
        data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'refno',
            'label': "ID",
            'fieldtype': 'int',
            'width': '60'
        },
        {
            'fieldname': 'full_name',
            'label': "Full Name",
            'fieldtype': 'Data',
            'width': '260'
        },
        {
            'fieldname': 'status',
            'label': "Status",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'date_of_joining',
            'label': "Date Of Joining",
            'fieldtype': 'Date',
            'width': '120'
        },
        {
            'fieldname': 'gender',
            'label': "Gender",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'email',
            'label': "Email",
            'fieldtype': 'Data',
            'width': '200'
        },
        {
            'fieldname': 'phone_number',
            'label': "Phone Number",
            'fieldtype': 'Data',
            'width': '180'
        },
        {
            'fieldname': 'division',
            'label': "Division",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'branch',
            'label': "Branch",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'basic_salary',
            'label': "Basic Salary",
            'fieldtype': 'currency',
            'width': '120'
        },
        {
            'fieldname': 'department',
            'label': "Department",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'designation',
            'label': "Position",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'employement_type',
            'label': "Employement Type",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'role',
            'label': "Role",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'birth_date',
            'label': "Birth Date",
            'fieldtype': 'Date',
            'width': '120'
        },
        {
            'fieldname': 'sub_city__zone',
            'label': "Subcity/Zone",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'woreda',
            'label': "Woreda",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'kebele',
            'label': "Kebele",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'house_number',
            'label': "House Number",
            'fieldtype': 'Data',
            'width': '120'
        },
    ]


def get_conditions(filters):
	conditions = ""

	if filters.get("division"):

		if filters['division'] == 'Branch':
			conditions += "division = '%s'" % filters["division"]
			if filters.get('branch'):
				conditions += "and branch = '%s'" % filters["branch"]

		if filters['division'] == 'Head Office':
			conditions += "division = '%s'" % filters["division"]

	return conditions

def get_employee_information(filters):
	conditions = get_conditions(filters)
	if filters.get("division"):
		if filters['division'] == 'Branch':

			return frappe.db.sql(
				f"""SELECT *
				FROM `tabEmployee`
				WHERE %s"""
				% conditions,
				as_dict=1,
			)
		elif filters['division'] == 'Head Office':
			return frappe.db.sql(
				f"""SELECT *
				FROM `tabEmployee`
				WHERE %s"""
				% conditions,
				as_dict=1,
			)
	else:
		return frappe.db.sql(
			f"""SELECT *
			FROM `tabEmployee`""",
			as_dict=1,
		)
