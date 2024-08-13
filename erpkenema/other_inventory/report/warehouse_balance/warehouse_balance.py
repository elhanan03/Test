# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    warehouse = get_warehouse_data(filters)

    if not warehouse:
        frappe.msgprint('No records found')
        return columns, warehouse

    for d in warehouse:
        row = frappe._dict({
            'date': d.date,
            'item_name': d.item_name,
            'item_category': d.item_category,
            'quantity': d.quantity,
            'uom': d.uom,
            'manufacturer': d.manufacturer,
            'brand': d.brand,
            'unit_cost': d.unit_cost,
            'total_cost': d.total_cost,
            'supplier_name': d.supplier_name,
            'remark': d.remark,

        })
        data.append(row)

    return columns, data


def get_columns():
    return [
       
        {
            "fieldname": "date",
            "fieldtype": "Date",
            "label": "Date",
            'width': '120'
        },
		{
            "fieldname": "item_name",
            "fieldtype": "Data",
            "label": "Item Name",
            'width': '120'
        },
        {
            "fieldname": "item_category",
            "fieldtype": "Link",
            "label": "Item Category",
            "options": "Item Category",
            'width': '120'
        },
        {
            "fieldname": "quantity",
            "fieldtype": "Float",
            "label": "Quantity",
            "non_negative": 1,
            "precision": "2",
            'width': '120'
        },
        {
            "fieldname": "uom",
            "fieldtype": "Link",
            "label": "UOM",
            "options": "UOM",
            'width': '120'
        },
        {
            "fieldname": "manufacturer",
            "fieldtype": "Data",
            "label": "Manufacturer",
            'width': '120'
        },
        {
            "fieldname": "brand",
            "fieldtype": "Data",
            "label": "Brand",
            'width': '120'
        },
        {
            "fieldname": "unit_cost",
            "fieldtype": "Float",
            "label": "Unit Cost",
            "non_negative": 1,
            "precision": "2",
            'width': '120'
        },
        {
            "fieldname": "total_cost",
            "fieldtype": "Float",
            "label": "Total Cost",
            "non_negative": 1,
            "precision": "2",
            'width': '120'
        },
        {
            "fieldname": "supplier_name",
            "fieldtype": "Data",
            "label": "Supplier Name",
            'width': '120'
        },
        {
            "fieldname": "remark",
            "fieldtype": "Data",
            "label": "Remark"
        },
    ]


def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += "date >= '%s'" % filters["from_date"]
    if filters.get("to_date"):
        conditions += "and date <= '%s'" % filters["to_date"]
    return conditions


def get_warehouse_data(filters):
    conditions = get_conditions(filters)
    if filters.get('from_date') and filters.get('to_date'):
        return frappe.db.sql(
            """select *
			from `tabWarehouse`
			where %s """
            % conditions,
            as_dict=1,
        )
    else:
        return frappe.db.sql(
            """select *
			from `tabWarehouse`""",
            as_dict=1,
        )
