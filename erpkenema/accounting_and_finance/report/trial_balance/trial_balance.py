# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    gl_entry_data = get_gl_entry_data(filters)

    if not gl_entry_data:
        frappe.msgprint('No records found')
        return columns, gl_entry_data
    balance = 0
    for d in gl_entry_data:
        closing_dr_amount = 0
        closing_cr_amount = 0
        if d.debit - d.credit >= 0:
            closing_dr_amount = d.debit - d.credit
            closing_cr_amount = 0
        else:
            closing_cr_amount = d.credit - d.debit
            closing_dr_amount = 0

        row = frappe._dict({
            'account': d.account_name,
            'opening_dr': 0,
            'opening_cr': 0,
            'debit': d.debit,
            'credit': d.credit,
            'closing_dr': closing_dr_amount,
            'closing_cr': closing_cr_amount
        })
        data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'account',
            'label': "Account",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'opening_dr',
            'label': "Opening(Dr)",
            'fieldtype': 'Currency',
            'width': '120'
        },
        {
            'fieldname': 'opening_cr',
            'label': "Opening(Cr)",
            'fieldtype': 'Currency',
            'width': '120'
        },
        {
            'fieldname': 'debit',
            'label': "Debit",
            'fieldtype': 'Currency',
            'width': '120'
        },
        {
            'fieldname': 'credit',
            'label': "Credit",
            'fieldtype': 'Currency',
            'width': '120'
        },
        {
            'fieldname': 'closing_dr',
            'label': "Closing(Dr)",
            'fieldtype': 'Currency',
            'width': '120'
        },

        {
            'fieldname': 'closing_cr',
            'label': "Closing(Cr)",
            'fieldtype': 'Currency',
            'width': '120'
        },
    ]


def get_conditions(filters):
    conditions = ""
    # if not filters.get("from_date"):
    # 	frappe.throw(_("'From Date' is required"))
    # else:
    # 	conditions += "exp_date >= '%s'" % filters["from_date"]
    # if filters.get("to_date"):
    # 	conditions += "and exp_date <= '%s'" % filters["to_date"]
    # else:
    # 	frappe.throw(_("'To Date' is required"))

    return conditions


def get_gl_entry_data(filters):
    return frappe.db.sql(
        f""" select account_name, sum(debit) as debit, sum(credit) as credit from `tabGL Entry` group by account_name""",
        as_dict=1,
    )
