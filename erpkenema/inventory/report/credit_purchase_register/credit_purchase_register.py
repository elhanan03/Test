# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe


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
            'purchase_invoice_number': d.purchase_invoice_number,
            'supplier_tin_number': d.supplier_tin_number,
            'cash_register_number': d.cash_register_number,
            'fs_date': d.fs_date,
			'date': d.date,
			'grv_no': d.name,
			'debit': d.total,
			'credit': d.total,
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
            'fieldname': 'purchase_invoice_number',
            'label': "FS Number",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'supplier_tin_number',
            'label': "TIN Number",
            'fieldtype': 'Data',
            'width': '120'
        },

        {
            'fieldname': 'cash_register_number',
            'label': "Cash Register Number",
            'fieldtype': 'Data',
            'width': '120'
        },

        {
            'fieldname': 'fs_date',
            'label': "FS Date",
            'fieldtype': 'date',
            'width': '120'
        }, 
		{
            'fieldname': 'date',
            'label': "GRV Date",
            'fieldtype': 'date',
            'width': '120'
        }, 
		{
            'fieldname': 'grv_no',
            'label': "GRV Number",
            'fieldtype': 'data',
            'width': '120'
        },
		{
            'fieldname': 'debit',
            'label': "Purchase (Debit)",
            'fieldtype': 'float',
            'width': '120'
        },
		{
            'fieldname': 'credit',
            'label': "Trade Creditor (credit)",
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

    if filters.get("branch_number"):
        conditions += "and branch_number = '%s'" % filters["branch_number"]
    return conditions


def get_good_receiving_voucher(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql(
        """select *
		from `tabGood Receiving Voucher`
		where %s and purchase_type = 'Credit Purchase'"""
        % conditions,
        as_dict=1,
    )
