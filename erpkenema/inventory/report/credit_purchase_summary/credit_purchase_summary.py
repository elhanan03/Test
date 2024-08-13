# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    credit_purchase_register = get_credit_purchase_register(filters)

    if not credit_purchase_register:
        frappe.msgprint('No records found')
        return columns, credit_purchase_register

    for d in credit_purchase_register:
        row = frappe._dict({
            'supplier_name': d.supplier_name,
			'total': d.credit,
			'branch_number': d.branch_number,
	
        })
        data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'branch_number',
            'label': "Branch",
            'fieldtype': 'data',
            'width': '120',
			
        },
		{
            'fieldname': 'supplier_name',
            'label': "Name of Suppliers",
            'fieldtype': 'Data',
            'width': '120'
        },
        
		{
            'fieldname': 'total',
            'label': "Total",
            'fieldtype': 'float',
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

    if filters.get("branch_number"):
        conditions += "and branch_number = '%s'" % filters["branch_number"]

    return conditions


def get_credit_purchase_register(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql(
        """select supplier_name, sum(credit) as credit, branch_number from `tabCredit Purchase Register` where %s group
by supplier_name;""" % conditions,
        as_dict=1,
    )
