# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt


import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    organization = get_organization(filters)

    if not organization:
        frappe.msgprint('No records found')
        return columns, organization

    for d in organization:
        row = frappe._dict({
            'organization_type': d.organization_type,
            'name1': d.name1,
            'tin_number': d.tin_number,
            'bank_account_no': d.bank_account_no,
            'email': d.email,
            'phone': d.phone,
            'focal_person': d.focal_person,
            'full_name': d.full_name,
            'address': d.address,
            'woreda': d.woreda,
            'house_number': d.house_number,
           
        })
        data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'name1',
            'label': "Name",
            'fieldtype': 'Data',
            'width': '200'
        },
        {
            'fieldname': 'tin_number',
            'label': "Tin Numver",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'bank_account_no',
            'label': "Bank Account Number",
            'fieldtype': 'Data',
            'width': '200'
        },
        {
            'fieldname': 'email',
            'label': "Email",
            'fieldtype': 'Data',
            'width': '200'
        },
        {
            'fieldname': 'phone',
            'label': "Phone",
            'fieldtype': 'Data',
            'width': '200'
        },
        {
            'fieldname': 'organization_type',
            'label': "Organization_type",
            'fieldtype': 'Data',
            'width': '200'
        },
        {
            'fieldname': 'focal_person',
            'label': "Focal Person",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'full_name',
            'label': "Full Name",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'address',
            'label': "Address",
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
            'fieldname': 'house_number',
            'label': "House Number",
            'fieldtype': 'Data',
            'width': '120'
        },
       
    ]


def get_conditions(filters):
    conditions = ""

    if filters.get("organization_type"):
        conditions += "and organization_type = '%s'" % filters["organization_type"]

    return conditions


def get_organization(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql(
            f"""SELECT *
            FROM `tabOrganization`""",
            as_dict=1,
        )
