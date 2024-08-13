# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()

    gl_entry_asset_credit_data = get_gl_entry_asset_credit_data(filters)
    gl_entry_asset_debit_data = get_gl_entry_asset_debit_data(filters)

    gl_entry_liability_credit_data = get_gl_entry_liability_credit_data(
        filters)
    gl_entry_liability_debit_data = get_gl_entry_liability_debit_data(filters)

    gl_entry_equity_credit_data = get_gl_entry_equity_credit_data(filters)
    gl_entry_equity_debit_data = get_gl_entry_equity_debit_data(filters)

    total_asset, total_liability, total_equity = 0, 0, 0

    if gl_entry_asset_credit_data[0].credit:
        total_asset -= gl_entry_asset_credit_data[0].credit

    if gl_entry_asset_debit_data[0].debit:
        total_asset += gl_entry_asset_debit_data[0].debit

    if gl_entry_liability_credit_data[0].credit:
        total_liability += gl_entry_liability_credit_data[0].credit

    if gl_entry_liability_debit_data[0].debit:
        total_liability -= gl_entry_liability_debit_data[0].debit

    if gl_entry_equity_credit_data[0].credit:
        total_equity += gl_entry_equity_credit_data[0].credit

    if gl_entry_equity_debit_data[0].debit:
        total_equity -= gl_entry_equity_debit_data[0].debit

    row = frappe._dict({
        'total_asset': total_asset,
        'total_liability': total_liability,
        'total_equity': total_equity,
        'profit_loss': total_asset - (total_liability + total_equity),
    })
    data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'net_operation',
            'label': "Net Cash from Operations",
            'fieldtype': 'Currency',
            'width': '220',
        },
        {
            'fieldname': 'net_investing',
            'label': "Net Cash from Investing",
            'fieldtype': 'Currency',
            'width': '220'
        },
        {
            'fieldname': 'net_financing',
            'label': "Net Cash from Financing",
            'fieldtype': 'Currency',
            'width': '220'
        },
        {
            'fieldname': 'net_cash',
            'label': "Net Change in Cash",
            'fieldtype': 'Currency',
            'width': '220'
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


def get_gl_entry_asset_credit_data(filters):
    return frappe.db.sql(
        f""" select sum(credit) as credit from `tabGL Entry` where root='Asset' """,
        as_dict=1,
    )


def get_gl_entry_asset_debit_data(filters):
    return frappe.db.sql(
        f""" select sum(debit) as debit from `tabGL Entry` where root='Asset' """,
        as_dict=1,
    )


def get_gl_entry_liability_credit_data(filters):
    return frappe.db.sql(
        f""" select sum(credit) as credit from `tabGL Entry` where root='Liability' """,
        as_dict=1,
    )


def get_gl_entry_liability_debit_data(filters):
    return frappe.db.sql(
        f""" select sum(debit) as debit from `tabGL Entry` where root='Liability' """,
        as_dict=1,
    )


def get_gl_entry_equity_credit_data(filters):
    return frappe.db.sql(
        f""" select sum(credit) as credit from `tabGL Entry` where root='Equity' """,
        as_dict=1,
    )


def get_gl_entry_equity_debit_data(filters):
    return frappe.db.sql(
        f""" select sum(debit) as debit from `tabGL Entry` where root='Equity' """,
        as_dict=1,
    )
