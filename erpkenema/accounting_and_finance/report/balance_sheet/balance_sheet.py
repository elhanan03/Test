# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_balance_data(filters)
    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'total_asset',
            'label': "Total Asset",
            'fieldtype': 'Currency',
            'width': '120',
        },
        {
            'fieldname': 'total_liability',
            'label': "Total Liability",
            'fieldtype': 'Currency',
            'width': '120'
        },
        {
            'fieldname': 'total_equity',
            'label': "Total Equity",
            'fieldtype': 'Currency',
            'width': '120'
        },
        {
            'fieldname': 'profit_loss',
            'label': "Profit/Loss",
            'fieldtype': 'Currency',
            'width': '120'
        },
    ]


def get_balance_data(filters):
    total_asset = get_total_balance(filters, 'Asset')
    total_liability = get_total_balance(filters, 'Liability')
    total_equity = get_total_balance(filters, 'Equity')
    profit_loss = total_asset - (total_liability + total_equity)

    row = {
        'total_asset': total_asset,
        'total_liability': total_liability,
        'total_equity': total_equity,
        'profit_loss': profit_loss,
    }

    return [row]


def get_total_balance(filters, root):
    credit_field = 'credit' if root == 'Asset' else 'debit'
    debit_field = 'debit' if root == 'Asset' else 'credit'

    credit_data = frappe.db.get_value(
        'GL Entry', filters={'root': root}, fieldname=f'sum({credit_field})')
    debit_data = frappe.db.get_value(
        'GL Entry', filters={'root': root}, fieldname=f'sum({debit_field})')

    return (debit_data or 0) - (credit_data or 0)

# import frappe


# def execute(filters=None):
#     columns = get_columns()
#     data = get_balance_data(filters)
#     return columns, data


# def get_columns():
#     return [
#         {
#             'fieldname': 'account',
#             'label': "Account",
#             'fieldtype': 'Data',
#             'width': '200',
#         },
#         {
#             'fieldname': 'credit',
#             'label': "Credit",
#             'fieldtype': 'Currency',
#             'width': '120',
#         },
#         {
#             'fieldname': 'debit',
#             'label': "Debit",
#             'fieldtype': 'Currency',
#             'width': '120'
#         },
#         {
#             'fieldname': 'balance',
#             'label': "Balance",
#             'fieldtype': 'Currency',
#             'width': '120'
#         },
#     ]


# def get_balance_data(filters):
#     data = []

#     assets_credit = get_total_balance(filters, 'Asset', credit=True)
#     assets_debit = get_total_balance(filters, 'Asset', credit=False)
#     assets_balance = assets_debit - assets_credit

#     liabilities_credit = get_total_balance(filters, 'Liability', credit=True)
#     liabilities_debit = get_total_balance(filters, 'Liability', credit=False)
#     liabilities_balance = liabilities_credit - liabilities_debit

#     equity_credit = get_total_balance(filters, 'Equity', credit=True)
#     equity_debit = get_total_balance(filters, 'Equity', credit=False)
#     equity_balance = equity_credit - equity_debit

#     income_credit = get_total_balance(filters, 'Income', credit=True)
#     income_debit = get_total_balance(filters, 'Income', credit=False)
#     income_balance = income_credit - income_debit

#     expenses_credit = get_total_balance(filters, 'Expense', credit=True)
#     expenses_debit = get_total_balance(filters, 'Expense', credit=False)
#     expenses_balance = expenses_debit - expenses_credit

#     profit_loss_credit = income_credit - expenses_credit
#     profit_loss_debit = income_debit - expenses_debit
#     profit_loss_balance = profit_loss_debit - profit_loss_credit

#     data.append({
#         'account': 'Asset',
#         'credit': assets_credit,
#         'debit': assets_debit,
#         'balance': assets_balance,
#     })

#     data.append({
#         'account': 'Liability',
#         'credit': liabilities_credit,
#         'debit': liabilities_debit,
#         'balance': liabilities_balance,
#     })

#     data.append({
#         'account': 'Equity',
#         'credit': equity_credit,
#         'debit': equity_debit,
#         'balance': equity_balance,
#     })

#     data.append({
#         'account': 'Income',
#         'credit': income_credit,
#         'debit': income_debit,
#         'balance': income_balance,
#     })

#     data.append({
#         'account': 'Expense',
#         'credit': expenses_credit,
#         'debit': expenses_debit,
#         'balance': expenses_balance,
#     })

#     data.append({
#         'account': 'Profit and Loss',
#         'credit': profit_loss_credit,
#         'debit': profit_loss_debit,
#         'balance': profit_loss_balance,
#     })

#     return data


# def get_total_balance(filters, root, credit=True):
#     amount_field = 'credit' if credit else 'debit'
#     amount = frappe.db.get_value(
#         'GL Entry', filters={'root': root}, fieldname=f'sum({amount_field})')
#     return amount or 0

# import frappe


# def execute(filters=None):
#     columns = get_columns()
#     data = get_data(filters)
#     return columns, data


# def get_columns():
#     return [
#         {
#             'fieldname': 'posting_date',
#             'label': 'Posting Date',
#             'fieldtype': 'Date',
#             'width': '120'
#         },
#         {
#             'fieldname': 'voucher_type',
#             'label': 'Voucher Type',
#             'fieldtype': 'Data',
#             'width': '120'
#         },
#         {
#             'fieldname': 'voucher_no',
#             'label': 'Voucher No',
#             'fieldtype': 'Data',
#             'width': '120'
#         },
#         {
#             'fieldname': 'account_name',
#             'label': 'Account Name',
#             'fieldtype': 'Data',
#             'width': '200'
#         },
#         {
#             'fieldname': 'credit',
#             'label': 'Credit',
#             'fieldtype': 'Currency',
#             'width': '120'
#         },
#         {
#             'fieldname': 'debit',
#             'label': 'Debit',
#             'fieldtype': 'Currency',
#             'width': '120'
#         },
#         {
#             'fieldname': 'balance',
#             'label': 'Balance',
#             'fieldtype': 'Currency',
#             'width': '120'
#         }
#     ]


# def get_data(filters):
#     data = frappe.db.sql(
#         """
#         SELECT posting_date, voucher_type, voucher_no, account_name, credit, debit, balance
#         FROM `tabGL Entry`
#         WHERE root IN ('Asset', 'Liability', 'Equity', 'Income', 'Expense')
#         ORDER BY posting_date, voucher_type, voucher_no
#         """,
#         as_dict=True
#     )

#     return data
