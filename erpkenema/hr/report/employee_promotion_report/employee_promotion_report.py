# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt


import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    employee_information = get_employee_information()

    if not employee_information:
        frappe.msgprint('No records found')
        return columns, employee_information

    for d in employee_information:
        row = frappe._dict({
            'promotion_date': d.promotion_date,
            'refno': d.refno,
            'full_name': d.full_name,
         	'division': d.division,
            'branch': d.branch,
            'from_employement_type': d.from_employement_type,
            'to_employement_type': d.to_employement_type,

        })
        data.append(row)

    return columns, data


def get_columns():
    return [
      	{
            'fieldname': 'refno',
            'label': "Promo ID",
            'fieldtype': 'Data',
            'width': '80'
        },
        {
            'fieldname': 'full_name',
            'label': "Full Name",
            'fieldtype': 'Data',
            'width': '180'
        },
        {
            'fieldname': 'division',
            'label': "Division",
            'fieldtype': 'Data',
            'width': '120'
        },
      		{
            'fieldname': 'branch',
            'label': "Branch",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'from_employement_type',
            'label': "From Employement Type",
            'fieldtype': 'Data',
            'width': '120'
        },
    		  {
            'fieldname': 'promotion_date',
            'label': "Promotion Date",
            'fieldtype': 'date',
            'width': '140'
        },
      	{
            'fieldname': 'to_employement_type',
            'label': "To Employement Type",
            'fieldtype': 'Data',
            'width': '120'
        },
       
    ]


def get_employee_information():
	return frappe.db.sql(
            f"""SELECT *
			FROM `tabEmployee Promotion`""",
         			as_dict=1,
        )
