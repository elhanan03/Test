# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data

import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	attendance = get_attendance(filters)

	if not attendance:
		frappe.msgprint('No records found')
		return columns, attendance

	for d in attendance:
		row = frappe._dict({
			'date': d.date,
			'employee': d.employee,
			'status': d.status,
			'entry_detail': d.entry_detail,
			'exit_detail': d.exit_detail,
			'number_status': d.number_status
		})
		data.append(row)

	return columns, data

def get_columns():
	return [
		{
			'fieldname': 'date',
			'label': "date",
			'fieldtype': 'Date',
			'width': '120'
		},
		
		{
			'fieldname': 'employee',
			'label': "Employee",
			'fieldtype': 'Data',
			'width': '180'
		},
		{
			'fieldname': 'status',
			'label': "Status",
			'fieldtype': 'data',
			'width': '120'
		},
		{
			'fieldname': 'entry_detail',
			'label': "Entry Detail",
			'fieldtype': 'Data',
			'width': '120'
		},
		{
			'fieldname': 'exit_detail',
			'label': "Exit Detail",
			'fieldtype': 'Data',
			'width': '120'
		},
		{
			'fieldname': 'number_status',
			'label': "Present Date",
			'fieldtype': 'Int',
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

	return conditions


def get_attendance(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		"""select *
		from `tabAttendance`
		where %s"""
		% conditions,
		as_dict=1,
	)