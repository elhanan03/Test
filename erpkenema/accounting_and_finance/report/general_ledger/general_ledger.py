# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	gl_entry_data = get_gl_entry_data(filters)

	if not gl_entry_data:
		frappe.msgprint('No records found')
		return columns, gl_entry_data
	balance = 0
	for d in gl_entry_data:
		if d.debit:
			balance += d.debit
		if d.credit:
			balance -= d.credit

		row = frappe._dict({
			'posting_date': d.posting_date,
			'account': d.account_name,
			'debit': d.debit,
			'credit': d.credit,
			'balance': balance,
			
		})
		data.append(row)

	return columns, data


def get_columns():
	return [
		{
			'fieldname': 'posting_date',
			'label': "Posting Date",
			'fieldtype': 'date',
			'width': '200',
		},
		{
			'fieldname': 'account',
			'label': "Account",
			'fieldtype': 'Data',
			'width': '200'
		},
		{
			'fieldname': 'debit',
			'label': "Debit",
			'fieldtype': 'Currency',
			'width': '200'
		},
		{
			'fieldname': 'credit',
			'label': "Credit",
			'fieldtype': 'Currency',
			'width': '200'
		},
		{
			'fieldname': 'balance',
			'label': "Balance",
			'fieldtype': 'Currency',
			'width': '200'
		},
	]


def get_conditions(filters):
	conditions = ""
	# if not filters.get("from_date"):
	# 	frappe.throw(_("'From Date' is required"))
	# else:
	# 	conditions += "posting_date >= '%s'" % filters["from_date"]
	# if filters.get("to_date"):
	# 	conditions += "and posting_date <= '%s'" % filters["to_date"]
	# else:
	# 	frappe.throw(_("'To Date' is required"))

	return conditions


def get_gl_entry_data(filters):
	return frappe.db.sql(
		f""" select * from `tabGL Entry`""",
		as_dict=1,
	)
