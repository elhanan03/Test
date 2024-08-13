# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    good_return_note = get_good_return_note(filters)

    if not good_return_note:
        frappe.msgprint('No records found')
        return columns, good_return_note

    for d in good_return_note:
        row = frappe._dict({
            'supplier_name':d.supplier,
			'purchase_invoice_number': d.fs_no,
			'grn_no': d.name,
			'in_transit_debit': d.total,
			'from_branch_credit': d.total,
			'branch': d.branch,	
			
        })
        data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'supplier_name',
            'label': "Supplier Name",
            'fieldtype': 'Data',
            'width': '200'
        },
		 {
            'fieldname': 'purchase_invoice_number',
            'label': "Invoice Number",
            'fieldtype': 'Data',
            'width': '120'
        },
		{
            'fieldname': 'grn_no',
            'label': "GRV Number",
            'fieldtype': 'data',
            'width': '120'
        },
		{
            'fieldname': 'in_transit_debit',
            'label': " Debit ( Creditor )",
            'fieldtype': 'float',
            'width': '120'
        },
		{
            'fieldname': 'in_transit_credit',
            'label': "Credit ( Creditor)",
            'fieldtype': 'float',
            'width': '120'
        },
		{
            'fieldname': 'from_branch_debit',
            'label': "Debit (Debitor)",
            'fieldtype': 'float',
            'width': '120'
        },
		{
            'fieldname': 'from_branch_credit',
            'label': "Credit (Debitor)",
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

    if filters.get("from_branch"):
        conditions += "and branch = '%s'" % filters["branch"]
    return conditions


def get_good_return_note(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql(
        """select *
		from `tabGood Return Note`
		where %s"""
        % conditions,
        as_dict=1,
    )
