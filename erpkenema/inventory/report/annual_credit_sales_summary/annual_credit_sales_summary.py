# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
import datetime

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    credit_sales_data = []

    year = datetime.datetime.now().year
    
    for month in range(1, 13):
        start_date = datetime.datetime(year, month, 1)
        formatted_start_date = start_date.strftime("%Y-%m-%d")

        end_date = datetime.datetime(year, month % 12 + 1, 1) - datetime.timedelta(days=1)

        conditions = "date >= '%s' and date <= '%s'" % (formatted_start_date, formatted_end_date)

        # frappe.msgprint(str(conditions))
        credit_sales_data.append(get_credit_sales_data(filters, conditions))
    
    # frappe.msgprint(str(credit_sales_data[1]))
    # output = list(zip(credit_sales_data[0], credit_sales_data[1]))
    # frappe.msgprint(str(output))

    # for d in credit_sales_data[1]:
    #     row = frappe._dict({
    #             'branch': d.branch_number,
    #             'july': d.total,
    #     })
    #     data.append(row)

    for jul, aug in list(zip(
        credit_sales_data[0], credit_sales_data[1], 
    )):
        row = frappe._dict({
            'branch': jul['branch_number'],
            'july': jul['total'],
            'august': aug['total']
        })
        data.append(row)

    return columns, data


def get_columns():
    return [
         {
            'fieldname': 'branch',
            'label': "Branch",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'july',
            'label': "July-2022",
            'fieldtype': 'Currency',
            'width': '120'
        },
        {
            'fieldname': 'august',
            'label': "August-2022",
            'fieldtype': 'Currency',
            'width': '120'
        },
        {
            'fieldname': 'september',
            'label': "September-2022",
            'fieldtype': 'Currency',
            'width': '120'
        },
        {
            'fieldname': 'october',
            'label': "October-2022",
            'fieldtype': 'Currency',
            'width': '120'
        },
        {
            'fieldname': 'november',
            'label': "November-2022",
            'fieldtype': 'Currency',
            'width': '120'
        },
        {
            'fieldname': 'december',
            'label': "December-2022",
            'fieldtype': 'Currency',
            'width': '120'
        },
        {
            'fieldname': 'january',
            'label': "January-2023",
            'fieldtype': 'Currency',
            'width': '120'
        },
        {
            'fieldname': 'feburary',
            'label': "Feburary-2023",
            'fieldtype': 'Currency',
            'width': '120'
        },
        {
            'fieldname': 'march',
            'label': "March-2023",
            'fieldtype': 'Currency',
            'width': '120'
        },
        {
            'fieldname': 'april',
            'label': "April-2023",
            'fieldtype': 'Currency',
            'width': '120'
        },
        {
            'fieldname': 'may',
            'label': "May-2023",
            'fieldtype': 'Currency',
            'width': '120'
        },
        {
            'fieldname': 'june',
            'label': "June-2023",
            'fieldtype': 'Currency',
            'width': '120'
        },
    ]


def get_credit_sales_data(filters, conditions):
    return frappe.db.sql(
            f"""select branch_number, sum(total_inc_vat) as total from `tabSales Attachment` where sales_type = 'Credit Sales' and %s group by branch_number"""
            % conditions,
            as_dict=1,
        )
   
