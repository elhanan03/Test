# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()

	gl_entry_income_credit_data = get_gl_entry_income_credit_data(filters)
	gl_entry_income_debit_data = get_gl_entry_income_debit_data(filters)

	gl_entry_expense_credit_data = get_gl_entry_expense_credit_data(filters)
	gl_entry_expense_debit_data = get_gl_entry_expense_debit_data(filters)	

	total_income, total_expense = 0, 0

	if gl_entry_income_credit_data[0].credit:	
		total_income += gl_entry_income_credit_data[0].credit 
	
	if gl_entry_income_debit_data[0].debit:
		total_income -= gl_entry_income_debit_data[0].debit

	if gl_entry_expense_credit_data[0].credit:
		total_expense -= gl_entry_expense_credit_data[0].credit 

	if gl_entry_expense_debit_data[0].debit:
		total_expense += gl_entry_expense_debit_data[0].debit
	
	
	row = frappe._dict({
			'total_income': total_income,
			'total_expense': total_expense,
			'profit_loss': total_income - total_expense,
	})
	data.append(row)

	return columns, data


def get_columns():
	return [
		{
			'fieldname': 'total_income',
			'label': "Total Income",
			'fieldtype': 'Currency',
			'width': '120',
		},
		{
			'fieldname': 'total_expense',
			'label': "Total Expense",
			'fieldtype': 'Currency',
			'width': '120'
		},
		{
			'fieldname': 'profit_loss',
			'label': "Profit/Loss",
			'fieldtype': 'Currency',
			'width': '120'
		},
	]


def get_conditions(filters):
	conditions = ""
	
	return conditions


def get_gl_entry_income_credit_data(filters):
	return frappe.db.sql(
		f""" select sum(credit) as credit from `tabGL Entry` where root='Income' """,
		as_dict=1,
	)

def get_gl_entry_income_debit_data(filters):
	return frappe.db.sql(
		f""" select sum(debit) as debit from `tabGL Entry` where root='Income' """,
		as_dict=1,
	)

def get_gl_entry_expense_credit_data(filters):
	return frappe.db.sql(
		f""" select sum(credit) as credit from `tabGL Entry` where root='Expense' """,
		as_dict=1,
	)
def get_gl_entry_expense_debit_data(filters):
	return frappe.db.sql(
		f""" select sum(debit) as debit from `tabGL Entry` where root='Expense' """,
		as_dict=1,
	)



