# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    petty_cash_payment__voucher = get_petty_cash_payment__voucher(filters)

    if not petty_cash_payment__voucher:
        frappe.msgprint('No records found')
        return columns, petty_cash_payment__voucher

    for d in petty_cash_payment__voucher:
        row = frappe._dict({
            'account_number': d.account_number,
            'date': d.date,
            'pcpv': d.name,
            'amount': d.payable_amounts_in_figure,
            'purpose': d.purpose,
        })
        data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'account_number',
            'label': "Account Number",
            'fieldtype': 'Data',
            'width': '140'
        },
        {
            'fieldname': 'date',
            'label': "Date",
            'fieldtype': 'Date',
            'width': '140'
        },
        {
            'fieldname': 'payee',
            'label': "Payee",
            'fieldtype': 'Data',
            'width': '140'
        },
        {
            'fieldname': 'pcpv',
            'label': "PCPV",
            'fieldtype': 'data',
            'width': '200'
        },

        {
            'fieldname': 'amount',
            'label': "Amount Paid",
            'fieldtype': 'float',
            'width': '120'
        },
        {
            'fieldname': 'purpose',
            'label': "Purpose",
            'fieldtype': 'Data',
            'width': '300'
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

    return conditions


def get_petty_cash_payment__voucher(filters):
    conditions = get_conditions(filters)
    print('i am here', conditions)
    return frappe.db.sql(
        """select * from `tabPetty Cash Payment  Voucher`
		where %s """
        % conditions,
        as_dict=1,
    )
