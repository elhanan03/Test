# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    inventory_area_store = get_inventory_area_store_data(filters)

    if not inventory_area_store:
        frappe.msgprint('No records found')
        return columns, inventory_area_store

    for d in inventory_area_store:
        row = frappe._dict({
            'branch': d.kenema_pharmacy_drug_shop_number,
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
        {
            'fieldname': 'branch',
            'label': "Branch",
            'fieldtype': 'Data',
            'width': '120'
        },
    ]


def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += "date >= '%s' " % filters["from_date"]
    if filters.get("to_date"):
        conditions += "and date <= '%s' " % filters["to_date"]
    if filters.get("branch"):
        conditions += "and kenema_pharmacy_drug_shop_number = '%s' " % filters["branch"]
    return conditions


def get_inventory_area_store_data(filters):
    conditions = get_conditions(filters)
    if filters.get('from_date') and filters.get('to_date') and filters.get('branch'):
        return frappe.db.sql(
            """select *
			from `tabInventory Area Store`
			where %s """
            % conditions,
            as_dict=1,
        )
    else:
        return frappe.db.sql(
            """select *
			from `tabInventory Area Store`""",
            as_dict=1,
        )


@frappe.whitelist()
def get_employee_branch(user):
    employee = frappe.get_all(
        "Employee", filters={"user_id": user, "status": "Active"}, fields=["branch"])
    return employee[0].branch if employee else None
