# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt


import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    over_time = get_over_time(filters)

    if not over_time:
        frappe.msgprint('No records found')
        return columns, over_time

    for d in over_time:
        row = frappe._dict({
            'requisition_section': d.requisition_section,
            'employee_name': d.employee_name,
            'from_date': d.from_date,
            'to_date': d.to_date,
            'division': d.division,
            'branch': d.branch,
            'designation': d.designation,
            'basic_salary': d.basic_salary,
            'working_time': d.name,
            'total_working_time': d.total_working_time,
            'total_payment': d.total_payment,

        })
        data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'requisition_number',
            'label': "ID",
            'fieldtype': 'int',
            'width': '60'
        },
        {
            'fieldname': 'employee_name',
            'label': "Full Name",
            'fieldtype': 'Data',
            'width': '200'
        },

        {
            'fieldname': 'from_date',
            'label': "From Date",
            'fieldtype': 'Date',
            'width': '120'
        },

        {
            'fieldname': 'to_date',
            'label': "To Date",
            'fieldtype': 'Date',
            'width': '120'
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
            'fieldname': 'designation',
            'label': "Position",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'basic_salary',
            'label': "Basic Salary",
            'fieldtype': 'Currency',
            "precision": "2",
            "options": "account.currency",
            'width': '120'
        },
        {
            'fieldname': 'working_time',
            'label': "Working Time",
            'fieldtype': 'Link',
            "options": "Over Time",
            "precision": "2",
            'width': '120'

        },
        {
            'fieldname': 'total_working_time',
            'label': "Total Working Time",
            'fieldtype': 'Float',
            "precision": "2",
            'width': '120'
        },
        {
            'fieldname': 'total_payment',
            'label': "Total payment",
            'fieldtype': 'Currency',
            "precision": "2",
            "options": "account.currency",
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
        if filters.get("position"):
            conditions += "and designation = '%s'" % filters["designation"]

    return conditions


def get_over_time(filters):
    conditions = get_conditions(filters)
    if filters.get("division"):
        if filters['division'] == 'Branch':

            return frappe.db.sql(
                f"""SELECT *
                FROM `tabOver Time`
                WHERE %s"""
                % conditions,
                as_dict=1,
            )
        elif filters['division'] == 'Head Office':
            return frappe.db.sql(
                f"""SELECT *
                FROM `tabOver Time`
                WHERE %s"""
                % conditions,
                as_dict=1,
            )
    else:
        return frappe.db.sql(
            f"""SELECT *
            FROM `tabOver Time`""",
            as_dict=1,
        )
