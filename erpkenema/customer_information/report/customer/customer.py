# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt


import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    customer_information = get_customer_information(filters)

    if not customer_information:
        frappe.msgprint('No records found')
        return columns, customer_information

    for d in customer_information:
        row = frappe._dict({
            'id_number': d.id_number,
            'full_name': d.full_name,
            'insurance_coverage_company': d.insurance_coverage_company,
            'customer_type': d.customer_type,
            'gender': d.gender,
            'phone_number': d.phone_number,
            'email': d.email,
            'regionstate': d.regionstate,
            'subcity': d.subcity,
            'woreda': d.woreda,
            'kebele': d.kebele,
            'house_number': d.house_number,
        })
        data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'id_number',
            'label': "ID Number",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'customer_type',
            'label': "Customer Type",
            'fieldtype': 'data',
            'width': '180'
        },
        {
            'fieldname': 'full_name',
            'label': "Full Name",
            'fieldtype': 'Data',
            'width': '260'
        },
        {
            'fieldname': 'gender',
            'label': "Gender",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'email',
            'label': "Email",
            'fieldtype': 'Data',
            'width': '200'
        },
        {
            'fieldname': 'phone_number',
            'label': "Phone Number",
            'fieldtype': 'Data',
            'width': '180'
        },
        {
            'fieldname': 'insurance_coverage_company',
            'label': "Organization",
            'fieldtype': 'Link',
            'options': 'Organization',
            'fieldtype': 'Data',
            'width': '120'
        },
    {
            'fieldname': 'regionstate',
            'label': "Region/State",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'subcity',
            'label': "Subcity/Zone",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'woreda',
            'label': "Woreda",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'kebele',
            'label': "Kebele",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'house_number',
            'label': "House Number",
            'fieldtype': 'Data',
            'width': '120'
        },
    ]


def get_conditions(filters):
    conditions = ""

    if filters.get("customer_type"):

        if filters['customer_type'] == 'Credit Customer':
            conditions += "customer_type = '%s'" % filters["customer_type"]
            if filters.get('Credit Customer'):
                conditions += "and Credit Customer = '%s'" % filters["Credit Customer"]

        if filters['customer_type'] == 'Cash Customer':
            conditions += "customer_type = '%s'" % filters["customer_type"]
       
        if filters.get("organization"):
            conditions += "and insurance_coverage_company = '%s'" % filters["organization"]

    return conditions


def get_customer_information(filters):
    conditions = get_conditions(filters)
    if filters.get("customer_type"):
        if filters['customer_type'] == 'Credit Customer':

            return frappe.db.sql(
                f"""SELECT *
                FROM `tabCustomer Information`
                WHERE %s"""
                % conditions,
                as_dict=1,
            )
        elif filters['customer_type'] == 'Cash Customer':
            return frappe.db.sql(
                f"""SELECT *
                FROM `tabCustomer Information`
                WHERE %s"""
                % conditions,
                as_dict=1,
            )
    else:
        return frappe.db.sql(
            f"""SELECT *
            FROM `tabCustomer Information`""",
            as_dict=1,
        )
