# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    sales_summary = get_sales_summary(filters)

    if not sales_summary:
        frappe.msgprint('No records found')
        return columns, sales_summary

    for d in sales_summary:
        row = frappe._dict({
            'date': d.sales_date,
            'branch': d.branch,
            'sales_breakdown': d.sales_breakdown,
            'total_cash_over': d.total_cash_over,
            'total_cash_short': d.total_cash_short,
            'sales_ticket_amount': d.sales_ticket_amount,
            'total_vat': d.total_vat,
            'actual_cash_deposit': d.actual_cash_deposit,
            'adjusted_sales_amount': d.adjusted_sales_amount,
            'body_weight': d.body_weight,
            'compounding_fee': d.compounding_fee,
            'packing_fee': d.packing_fee,
            'others': d.others,



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
            'fieldname': 'branch',
            'label': "Branch",
            'fieldtype': 'Data',
            'width': '120'
        }, {
            'fieldname': 'sales_breakdown',
            'label': "Sales Breakdown",
            'fieldtype': 'data',
            'width': '120'
        },

        {
            'fieldname': 'total_cash_over',
            'label': "Total Cash Over",
            'fieldtype': 'Float',
            'width': '120'
        },
        {
            'fieldname': 'total_cash_short',
            'label': "Total Cash short",
            'fieldtype': 'Float',
            'width': '120'
        },
        {
            'fieldname': 'sales_ticket_amount',
            'label': "Sales Ticket Amount",
            'fieldtype': 'Float',
            'width': '120'
        },
        {
            'fieldname': 'total_vat',
            'label': "Total VAT",
            'fieldtype': 'Float',
            'width': '120'
        },
        {
            'fieldname': 'actual_cash_deposit',
            'label': "Actual Cash Deposit",
            'fieldtype': 'Float',
            'width': '120'
        },
        {
            'fieldname': 'adjusted_sales_amount',
            'label': "Adjusted Sales Amount",
            'fieldtype': 'Float',
            'width': '120'
        },
        {
            'fieldname': 'body_weight',
            'label': "Body Weight",
            'fieldtype': 'Float',
            'width': '120'
        },
        {
            'fieldname': 'compounding_fee',
            'label': "Compounding Fee",
            'fieldtype': 'Float',
            'width': '120'
        },
        {
            'fieldname': 'packing_fee',
            'label': "Packing Fee",
            'fieldtype': 'Float',
            'width': '120'
        },
        {
            'fieldname': 'others',
            'label': "Others",
            'fieldtype': 'Float',
            'width': '120'
        },
    ]


def get_conditions(filters):
    conditions = ""
    if not filters.get("date"):
        frappe.throw(_("'Date' is required"))
    else:
        conditions = "sales_date = '%s'" % filters["date"]
    if filters.get("branch"):
        conditions += "and branch = '%s'" % filters["branch"]

    return conditions


def get_sales_summary(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql(
        """select *
		from `tabDaily Cash sales Summary`
		where %s"""
        % conditions,
        as_dict=1,
    )
