# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpkenema.api import get_employee_data

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    credit_sales_data = get_credit_sales_data(filters)

    if not credit_sales_data:
        frappe.msgprint('No records found')
        return columns, credit_sales_data

    for d in credit_sales_data:
        row = frappe._dict({
            'date': d.date,
            'invoice.no': d.name,
            'to': d.full_name,
            'id': d.id_number,
            'organization': d.organization,
            'branch_number': d.branch_number,
            'total_inc_vat': d.total_inc_vat,

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
            'fieldname': 'id',
            'label': "CBHI ID",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'organization',
            'label': "Organization",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'branch_number',
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

    if filters.get("organization"):
        conditions += "and organization = '%s'" % filters["organization"]
    return conditions

def get_credit_sales_data(filters):
    conditions = get_conditions(filters)
    
    return frappe.db.sql(
        """select *
		from `tabSales Attachment`
		where sales_type ='Credit Sales' and %s"""
        % conditions,
        as_dict=1,
    )