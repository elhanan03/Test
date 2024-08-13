# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpkenema.api import get_employee_data

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    inventory_area_store = get_inventory_area_store(filters)

    if not inventory_area_store:
        frappe.msgprint('No records found')
        return columns, inventory_area_store

    for d in inventory_area_store:
        row = frappe._dict({
            'supplier_name': "From "+ str(d.kenema_pharmacy_drug_shop_number)+" To "+str(d.kenema_pharmacy_drug_shop_number),
			'stm_no': d.name,
			'transfer_in_debit': d.total_purchase_cost,
			'transfer_out_credit': d.total_purchase_cost,
			'branch_number': d.kenema_pharmacy_drug_shop_number,
			
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
            'fieldname': 'transfer_in_debit',
            'label': " Debit ( Transfer in)",
            'fieldtype': 'float',
            'width': '120'
        },
		{
            'fieldname': 'transfer_in_credit',
            'label': "Credit ( Transfer In)",
            'fieldtype': 'float',
            'width': '120'
        },
		{
            'fieldname': 'transfer_out_debit',
            'label': "Debit (Transfer In Transit)",
            'fieldtype': 'float',
            'width': '120'
        },
		{
            'fieldname': 'transfer_out_credit',
            'label': "Credit (Transfer_In Transit)",
            'fieldtype': 'float',
            'width': '120'
        },
		{
            'fieldname': 'branch_number',
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
            conditions += "and kenema_pharmacy_drug_shop_number = '%s'" % data[0].branch
        else:
            if filters.get("branch_number"):
                conditions += "and kenema_pharmacy_drug_shop_number = '%s'" % filters["branch_number"]
    else:
        if filters.get("branch_number"):
            conditions += "and kenema_pharmacy_drug_shop_number = '%s'" % filters["branch_number"]
            
    return conditions


def get_inventory_area_store(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql(
        """select *
		from `tabInventory Area Store`
		where %s and purchase_type = 'Transfer In'"""
        % conditions,
        as_dict=1,
    )
