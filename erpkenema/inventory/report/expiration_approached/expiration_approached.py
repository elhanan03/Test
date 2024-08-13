# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	ias_data = get_ias_data(filters)

	if not ias_data:
		frappe.msgprint('No records found')
		return columns, ias_data

	for d in ias_data:
		row = frappe._dict({
			'item_code': d.item_code,
			'batch_number': d.batch_number,
			'description': d.description,
			'unit': d.unit,
			'quantity': d.quantity,
			'unit_purchase_cost': d.unit_purchase_cost,
			'total_purchase_cost': d.total_purchase_cost,
			'date': d.date,
			'exp_date': d.exp_date,
			'supplier_name': d.supplier_name
		})
		data.append(row)

	return columns, data

def get_columns():
	return [
		{
			'fieldname': 'item_code',
			'label': "Item Code",
			'fieldtype': 'Data',
			'width': '120',
		},
		{
			'fieldname': 'batch_number',
			'label': "Batch Number",
			'fieldtype': 'Data',
			'width': '120'
		},
		{
			'fieldname': 'description',
			'label': "Description",
			'fieldtype': 'Data',
			'width': '120'
		},
		{
			'fieldname': 'unit',
			'label': "Unit",
			'fieldtype': 'Data',
			'width': '120'
		},
		{
			'fieldname': 'quantity',
			'label': "Quantity",
			'fieldtype': 'Int',
			'width': '120'
		},
		{
			'fieldname': 'unit_purchase_cost',
			'label': "Unit Purchase Cost",
			'fieldtype': 'Float',
			'width': '120'
		},
		{
			'fieldname': 'date',
			'label': "Entry Date",
			'fieldtype': 'Date',
			'width': '120'
		},
		{
			'fieldname': 'exp_date',
			'label': "Expiry Date",
			'fieldtype': 'Date',
			'width': '120'
		},
		{
			'fieldname': 'supplier_name',
			'label': "Supplier Name",
			'fieldtype': 'Data',
			'width': '120'
		},
	]


def get_conditions(filters):
	conditions = ""
	if not filters.get("from_date"):
		frappe.throw(_("'From Date' is required"))
	else:
		conditions += "exp_date >= '%s'" % filters["from_date"]
	if filters.get("to_date"):
		conditions += "and exp_date <= '%s'" % filters["to_date"]
	else:
		frappe.throw(_("'To Date' is required"))

	return conditions


def get_ias_data(filters):
	conditions = get_conditions(filters)
	doc = "`tab"+filters["store"]+"`"
	return frappe.db.sql(
		f"""select item_code,batch_number,description,unit,quantity,unit_purchase_cost,date,exp_date,supplier_name
		from {doc}
		where %s"""
		% conditions,
		as_dict=1,
	)	