# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpkenema.api import get_employee_data

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    good_return_note = get_good_return_note(filters)

    if not good_return_note:
        frappe.msgprint('No records found')
        return columns, good_return_note

    for d in good_return_note:
        row = frappe._dict({
            'supplier_name': d.supplier,
            'consignment_number': d.consignment_number,
			'grn_no': d.name,
			'other_income_credit': d.total,
			'supplier_debit': d.total,
			'branch': d.branch,
			

        })
        data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'supplier_name',
            'label': "Name of Suppliers",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'consignment_number',
            'label': "Cons. Note",
            'fieldtype': 'Data',
            'width': '120'
        },
		{
            'fieldname': 'grn_no',
            'label': "GRN Number",
            'fieldtype': 'data',
            'width': '120'
        },
		{
            'fieldname': 'other_income_debit',
            'label': " Debit (Other Income))",
            'fieldtype': 'float',
            'width': '120'
        },
		{
            'fieldname': 'other_income_credit',
            'label': "Credit (Other Income))",
            'fieldtype': 'float',
            'width': '120'
        },
		{
            'fieldname': 'supplier_debit',
            'label': "Debit (Trade Creditor)",
            'fieldtype': 'float',
            'width': '120'
        },
		{
            'fieldname': 'supplier_credit',
            'label': "Credit (Trade Creditor)",
            'fieldtype': 'float',
            'width': '120'
        },
		{
            'fieldname': 'branch',
            'label': "Branch",
            'fieldtype': 'data',
            'width': '120',
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

    data = get_employee_data()

    if data:
        if data[0].division =='Branch':
            conditions += "and branch = '%s'" % data[0].branch
        else:
            if filters.get("branch"):
                conditions += "and branch = '%s'" % filters["branch"]
    else:
        if filters.get("branch"):
            conditions += "and branch = '%s'" % filters["branch"]

    if filters.get("branch"):
        conditions += "and branch= '%s'" % filters["branch"]
    return conditions


def get_good_return_note(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql(
        """select *
		from `tabGood Return Note`
		where %s and return_type = 'Consignment Out'"""
        % conditions,
        as_dict=1,
    )