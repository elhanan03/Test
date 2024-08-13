# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	purchase_request_for_drug_and_medical_supplies = get_purchase_request_for_drug_and_medical_supplies_data(filters)

	if not purchase_request_for_drug_and_medical_supplies:
		frappe.msgprint('No records found')
		return columns, purchase_request_for_drug_and_medical_supplies

	for d in purchase_request_for_drug_and_medical_supplies:
		row = frappe._dict({
			'item_code': d.item_code,
			'description': d.description,
			'batch_number': d.batch_number,
			'quantity': d.quantity,
			'unit': d.unit,
			'brand': d.brand,
			'unit_purchase_cost': d.unit_purchase_cost,
			'total_purchase_cost': d.total_purchase_cost,
			'unit_selling_price': d.unit_selling_price,
			'exp_date': d.exp_date,
			'supplier': d.supplier,
			'purchase_type': d.purchase_type

		})
		data.append(row)

	return columns, data


def get_columns():
	return [
		{
			'fieldname': 'item_code',
			'label': "Item Code",
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
			'fieldname': 'batch_number',
			'label': "Batch Number",
			'fieldtype': 'data',
			'width': '120'
		},
		{
			'fieldname': 'quantity',
			'label': "Quantity",
			'fieldtype': 'int',
			'width': '120'
		},
		{
			'fieldname': 'unit',
			'label': "Unit",
			'fieldtype': 'Data',
			'width': '120'
		},
		{
			'fieldname': 'brand',
			'label': "Brand",
			'fieldtype': 'Data',
			'width': '120'
		},
		{
			'fieldname': 'unit_purchase_cost',
			'label': "Unit Purchase Cost",
			'fieldtype': 'float',
			'width': '120'
		},
		{
			'fieldname': 'total_purchase_cost',
			'label': "Total Purchase Cost",
			'fieldtype': 'float',
			'width': '120'
		},
		{
			'fieldname': 'unit_selling_price',
			'label': "Unit Selling Price",
			'fieldtype': 'float',
			'width': '120'
		},
		{
			'fieldname': 'exp_date',
			'label': "Expiry Date",
			'fieldtype': 'Date',
			'width': '120'
		},
		{
			'fieldname': 'supplier',
			'label': "Supplier",
			'fieldtype': 'Data',
			'width': '120'
		},
		{
			'fieldname': 'purchase_type',
			'label': "Purchase Type",
			'fieldtype': 'Data',
			'width': '120'
		},
	]


def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += "date >= '%s'" % filters["from_date"]
	if filters.get("to_date"):
		conditions += "and date <= '%s'" % filters["to_date"]
	return conditions


def get_purchase_request_for_drug_and_medical_supplies_data(filters):
	conditions = get_conditions(filters)
	if filters.get('from_date') and filters.get('to_date'):
		return frappe.db.sql(
			"""select *
			from `tabPurchase request for drug and medical supplies`
			where %s """
			% conditions,
			as_dict=1,
		)
	else:
		return frappe.db.sql(
			"""select *
			from `tabPurchase request for drug and medical supplies`""",
			as_dict=1,
		)
