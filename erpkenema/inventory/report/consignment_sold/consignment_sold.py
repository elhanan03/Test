# Copyright (c) 2023, TechEthio IT Solution plc and contributors
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
            'fs_no': d.purchase_invoice_number,
			'grv_no': d.name,
			'e_debit': d.total,
			'purchase_credit': d.total,
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
            'width': '150'
        },
        {
            'fieldname': 'fs_number',
            'label': "FS NO",
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
            'fieldname': 'e_debit',
            'label': " Debit (Other Income)",
            'fieldtype': 'float',
            'width': '150'
        },
		{
            'fieldname': 'e_credit',
            'label': "Credit (Other Income)",
            'fieldtype': 'float',
            'width': '150'
        },
		{
            'fieldname': 'purchase_debit',
            'label': "Debit (Trade of Creditors)",
            'fieldtype': 'float',
            'width': '150'
        },
		{
            'fieldname': 'purchase_credit',
            'label': "Credit (Trade of Creditors)",
            'fieldtype': 'float',
            'width': '150'
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
            if filters.get("branch"):
                conditions += "and branch_number = '%s'" % filters["branch"]
    else:
        if filters.get("branch"):
            conditions += "and branch_number = '%s'" % filters["branch"]

    return conditions


def get_good_receiving_voucher(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql(
        """select *
		from `tabGood Receiving Voucher`
		where %s and purchase_type = 'Discount'"""
        % conditions,
        as_dict=1,
    )
