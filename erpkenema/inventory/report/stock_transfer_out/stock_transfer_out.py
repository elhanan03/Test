# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpkenema.api import get_employee_data

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    stock_transfer_memo = get_stock_transfer_memo(filters)

    if not stock_transfer_memo:
        frappe.msgprint('No records found')
        return columns, stock_transfer_memo

    for d in stock_transfer_memo:
        row = frappe._dict({
            'supplier_name': "From "+ str(d.from_branch)+" To "+str(d.to_branch),
			'stm_no': d.name,
			'in_transit_debit': d.total,
			'transfer_credit': d.total,
			'from_branch': d.from_branch,
			
        })
        data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'supplier_name',
            'label': "Transfer",
            'fieldtype': 'Data',
            'width': '200'
        },
		{
            'fieldname': 'stm_no',
            'label': "STM Number",
            'fieldtype': 'data',
            'width': '120'
        },
		{
            'fieldname': 'in_transit_debit',
            'label': " Debit (Stock in Trancsit))",
            'fieldtype': 'float',
            'width': '120'
        },
		{
            'fieldname': 'in_transit_credit',
            'label': "Credit (Stock in transit))",
            'fieldtype': 'float',
            'width': '120'
        },
		{
            'fieldname': 'transfer_debit',
            'label': "Debit (Transfer)",
            'fieldtype': 'float',
            'width': '120'
        },
		{
            'fieldname': 'transfer_credit',
            'label': "Credit (Transfer)",
            'fieldtype': 'float',
            'width': '120'
        },
		{
            'fieldname': 'from_branch',
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
            conditions += "and from_branch = '%s'" % data[0].branch
        else:
            if filters.get("from_branch"):
                conditions += "and from_branch = '%s'" % filters["from_branch"]
    else:
        if filters.get("from_branch"):
            conditions += "and from_branch = '%s'" % filters["from_branch"]

    # if filters.get("from_branch"):
    #     conditions += "and from_branch = '%s'" % filters["from_branch"]

    return conditions


def get_stock_transfer_memo(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql(
        """select *
		from `tabStock Transfer Memo`
		where %s"""
        % conditions,
        as_dict=1,
    )
