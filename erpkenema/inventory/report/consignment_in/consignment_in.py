# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpkenema.api import get_employee_data

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    good_receiving_voucher = get_good_receiving_voucher(filters)

    if not good_receiving_voucher:
        frappe.msgprint('No records found')
        return columns, good_receiving_voucher

    for d in good_receiving_voucher:
        row = frappe._dict({
            'supplier_name': d.supplier_name,
            'consignment_number': d.consignment_number,
			'grv_no': d.name,
			'other_income_debit': d.total,
			'supplier_credit': d.total,
			'branch_number': d.branch_number,
			

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
            'fieldname': 'grv_no',
            'label': "GRV Number",
            'fieldtype': 'data',
            'width': '120'
        },
		{
            'fieldname': 'other_income_debit',
            'label': " Debit (Other Income)",
            'fieldtype': 'float',
            'width': '120'
        },
		{
            'fieldname': 'other_income_credit',
            'label': "Credit (Other Income)",
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
            'fieldname': 'branch_number',
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
            conditions += "and branch_number = '%s'" % data[0].branch
        else:
            if filters.get("branch_number"):
                conditions += "and branch_number = '%s'" % filters["branch_number"]
    else:
        if filters.get("branch_number"):
            conditions += "and branch_number = '%s'" % filters["branch_number"]

    return conditions


def get_good_receiving_voucher(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql(
        """select *
		from `tabGood Receiving Voucher`
		where %s and purchase_type = 'Consignment In'"""
        % conditions,
        as_dict=1,
    )
