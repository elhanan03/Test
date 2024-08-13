# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    action_plan = get_action_plan(filters)

    if not action_plan:
        frappe.msgprint('No records found')
        return columns, action_plan

    for d in action_plan:
        row = frappe._dict({
            'date': d.date,
        })
        data.append(row)

    return columns, data

def get_columns():
    return [
        {
            'fieldname': 'date',
            'label': "Date",
            'fieldtype': 'Date',
            'width': '120'
        },
        {
            'fieldname': 'date',
            'label': "Date",
            'fieldtype': 'Date',
            'width': '120'
        }, 
        {
            'fieldname': 'date',
            'label': "Date",
            'fieldtype': 'Date',
            'width': '120'
        },
         {
            'fieldname': 'date',
            'label': "Date",
            'fieldtype': 'Date',
            'width': '120'
        },
         {
            'fieldname': 'date',
            'label': "Date",
            'fieldtype': 'Date',
            'width': '120'
        },
         {
            'fieldname': 'date',
            'label': "Date",
            'fieldtype': 'Date',
            'width': '120'
        },
         {
            'fieldname': 'date',
            'label': "Date",
            'fieldtype': 'Date',
            'width': '120'
        },

        
		
    ]

def get_conditions(filters):
    conditions = ""
    if not filters.get("from_date"):
        frappe.throw(_("'From Date' is required"))
    else:
        conditions += "date >= '%s'" % filters["from_date"]
    if filters.get("to_date"):
        conditions += "and date <= '%s'" % filters["to_date"]
    else:
        frappe.throw(_("'To Date' is required"))
    return conditions

def get_action_plan(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql(
        """select * 
		From `tabAction Plan`
		where %s"""
        % conditions,
        as_dict=1,
    )