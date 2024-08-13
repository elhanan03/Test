# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpkenema.api import get_employee_data

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    expired_items_data = get_expired_items_data(filters)

    if not expired_items_data:
        frappe.msgprint('No records found')
        return columns, expired_items_data

    for d in expired_items_data:
        row = frappe._dict({
            'item_code': d.item_code,
            'description': d.description,
            'unit': d.unit,
            'quantity': d.quantity,
        })
        data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'item_code',
            'label': "Item Code",
            'fieldtype': 'Int',
            'width': '120'
        },
        {
            'fieldname': 'description',
            'label': "Description",
            'fieldtype': 'Data',
            'width': '180'
        },
        {
            'fieldname': 'unit',
            'label': "Unit",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'quantity',
            'label': "Quantity",
            'fieldtype': 'Int',
            'width': '80'
        },
    ]


def get_conditions(filters):
    conditions = ""
    if not filters.get("from_date"):
        frappe.throw(_("'From Date' is required"))
    else:
        conditions += "exp_date >= '%s'" % filters["from_date"]
    if filters.get("to_date"):
        conditions += "and exp_date <= '%s'" % filters["to_date"]
    else:
        frappe.throw(_("'To Date' is required"))

    data = get_employee_data()
    if data:
        if data[0].division =='Branch':
            conditions += "and branch_number = '%s'" % data[0].branch
        else:
            if filters.get("branch_number"):
                conditions += "and branch_number = '%s'" % filters["branch_number"]
    else:
        if filters.get("branch_number"):
            conditions += "and branch_number = '%s'" % filters["branch_number"]

    return conditions

def get_expired_items_data(filters):
    conditions = get_conditions(filters)
    
    return frappe.db.sql(
        """select *
		from `tabOut of service items`
		where type='Expired Item' and %s"""
        % conditions,
        as_dict=1,
    )
