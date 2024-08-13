# # Copyright (c) 2022, TechEthio IT Solution plc and contributors
# # For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	columns = get_columns()
# 	sas_data = get_sas_data(filters)

# 	if not sas_data:
# 		frappe.msgprint('No records found')
# 		return columns, sas_data

# 	for d in sas_data:
# 		row = frappe._dict({
# 			'description': d.description,
# 			'total_quantity': d.total_quantity,
# 			'total_price': d.total_price
# 		})
# 		data.append(row)

# 	return columns, data

# def get_columns():
# 	return [
# 		{
# 			'fieldname': 'description',
# 			'label': "Description",
# 			'fieldtype': 'Data',
# 			'width': '120',
# 		},
# 		{
# 			'fieldname': 'total_quantity',
# 			'label': "Sold Quantity",
# 			'fieldtype': 'int',
# 			'width': '120'
# 		},
# 		{
# 			'fieldname': 'total_price',
# 			'label': "Total Price",
# 			'fieldtype': 'Currency',
# 			'width': '120'
# 		},
# 	]


# def get_conditions(filters):
# 	conditions = ""
# 	if not filters.get("from_date"):
# 		frappe.throw(_("'From Date' is required"))
# 	else:
# 		conditions += "creation >= '%s'" % filters["from_date"]
	
# 	if not filters.get('to_date'):
# 		frappe.throw(_("'To Date' is required"))

# 	if filters.get("to_date"):
# 		conditions += "and creation <= '%s'" % filters["to_date"]

# 	return conditions


# def get_sas_data(filters):
# 	conditions = get_conditions(filters)
# 	if filters.get('from_date') and filters.get('to_date'):
# 		return frappe.db.sql(
# 			f"""SELECT description, SUM(quantity) as total_quantity, SUM(total_price) as total_price FROM `tabPurchased Medicine` where %s GROUP BY description ORDER BY total_quantity DESC;
# 			"""
# 			% conditions,
# 			as_dict=1,
# 		)	
# 	else:
# 		return frappe.db.sql(
# 			f"""
# 			SELECT description, SUM(quantity) as total_quantity, SUM(total_price) as total_price FROM `tabPurchased Medicine` GROUP BY description ORDER BY total_quantity DESC;
# 			""", 
# 			as_dict=1
# 		)


# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    abc_data = get_abc_data(filters)

    if not abc_data:
        frappe.msgprint('No records found')
        return columns, abc_data

    for d in abc_data:
        row = frappe._dict({
            'description': d.description,
            'total_quantity': d.total_quantity,
            'total_price': d.total_price,
            'abc_category': d.abc_category
        })
        data.append(row)

    return columns, data

def get_columns():
    return [
        {
            'fieldname': 'description',
            'label': "Description",
            'fieldtype': 'Data',
            'width': '120',
        },
        {
            'fieldname': 'total_quantity',
            'label': "Total Quantity",
            'fieldtype': 'Int',
            'width': '120'
        },
        {
            'fieldname': 'total_price',
            'label': "Total Price",
            'fieldtype': 'Currency',
            'width': '120'
        },
        {
            'fieldname': 'abc_category',
            'label': "ABC Category",
            'fieldtype': 'Data',
            'width': '120'
        },
    ]

def get_conditions(filters):
    conditions = ""
    if not filters.get("from_date"):
        frappe.throw(_("'From Date' is required"))
    else:
        conditions += "creation >= '%s'" % filters["from_date"]
    
    if not filters.get('to_date'):
        frappe.throw(_("'To Date' is required"))

    if filters.get("to_date"):
        conditions += " and creation <= '%s'" % filters["to_date"]

    return conditions

def get_abc_data(filters):
    conditions = get_conditions(filters)
    if filters.get('from_date') and filters.get('to_date'):
        sas_data = frappe.db.sql(
            f"""SELECT description, SUM(quantity) as total_quantity, SUM(total_price) as total_price
                FROM `tabPurchased Medicine`
                WHERE {conditions}
                GROUP BY description
                ORDER BY total_price DESC""",
            as_dict=1,
        )
    else:
        sas_data = frappe.db.sql(
            f"""SELECT description, SUM(quantity) as total_quantity, SUM(total_price) as total_price
                FROM `tabPurchased Medicine`
                GROUP BY description
                ORDER BY total_price DESC""",
            as_dict=1
        )

    # Calculate cumulative total price and determine ABC category
    total_value = sum(item['total_price'] for item in sas_data)
    cumulative_value = 0
    for item in sas_data:
        cumulative_value += item['total_price']
        cumulative_percentage = (cumulative_value / total_value) * 100

        if cumulative_percentage <= 70:
            item['abc_category'] = 'A'
        elif cumulative_percentage <= 90:
            item['abc_category'] = 'B'
        else:
            item['abc_category'] = 'C'

    return sas_data
