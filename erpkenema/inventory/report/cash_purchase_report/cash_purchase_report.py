# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	grv_data = get_grv_data(filters)

	if not grv_data:
		frappe.msgprint('No records found')
		return columns, grv_data

	for d in grv_data:
		row = frappe._dict({
			'date': d.date,
			'grv.no': d.name,
     		'supplier': d.supplier_name,
			'total': d.total

		})
		data.append(row)

	return columns, data

def get_columns():
	return [
		{
			'fieldname': 'date',
			'label': "Purchase Date",
			'fieldtype': 'Date',
			'width': '120'
		},
		{
			'fieldname': 'grv.no',
			'label': "GRV No.",
			'fieldtype': 'Link',
			'options': 'Good Receiving Voucher',
			'width': '180'
    	},
		{
			'fieldname': 'supplier',
			'label': 'Supplier',
			'fieldtype': 'Data',
			'width': '180'
    	},
		{
			'fieldname': 'total',
			'label': "Total",
			'fieldtype': 'Currency',
			'width': '120'
		},
	]


def get_conditions(filters):
	conditions = "purchase_type='Cash Purchase' and "
	
	if not filters.get("from_date"):
		frappe.throw(_("'From Date' is required"))
	else:
		conditions += "date >= '%s'" % filters["from_date"]
	if filters.get("to_date"):
		conditions += "and date <= '%s'" % filters["to_date"]
	else:
		frappe.throw(_("'To Date' is required"))


	return conditions

def get_grv_data(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		"""select *
		from `tabGood Receiving Voucher`
		where %s"""
		% conditions,
		as_dict=1,
	)
