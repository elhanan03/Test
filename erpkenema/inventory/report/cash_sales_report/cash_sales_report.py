# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpkenema.api import get_employee_data

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    cash_sales_data = get_cash_sales_data(filters)

    if not cash_sales_data:
        frappe.msgprint('No records found')
        return columns, cash_sales_data

    for d in cash_sales_data:
        row = frappe._dict({
            'date': d.date,
            'invoice.no': d.name,
            'branch': d.branch_number,
            'to': d.full_name,
            'total_inc_vat': d.total_inc_vat
        })
        data.append(row)

    return columns, data

def get_columns():
    return [
        {
            'fieldname': 'date',
            'label': "Sales Date",
            'fieldtype': 'Date',
            'width': '120'
        },
        {
            'fieldname': 'invoice.no',
            'label': "Invoice No.",
            'fieldtype': 'Link',
            'options': 'Sales Attachment',
            'width': '180'
        },

        {
            'fieldname': 'to',
            'label': "To",
            'fieldtype': 'Data',
            'width': '180'
        },
        {
            'fieldname': 'branch',
            'label': "Branch",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'total_inc_vat',
            'label': "Total Inc. Vat",
            'fieldtype': 'Currency',
            'width': '120'
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
            conditions += "and branch_number = '%s'" % data[0].branch
        else:
            if filters.get("branch_number"):
                conditions += "and branch_number = '%s'" % filters["branch_number"]
    else:
        if filters.get("branch_number"):
            conditions += "and branch_number = '%s'" % filters["branch_number"]
    
    return conditions


def get_cash_sales_data(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql(
        """select *
        from `tabSales Attachment`
        where sales_type ='Cash Sales' and %s"""
        % conditions,
        as_dict=1,
    )