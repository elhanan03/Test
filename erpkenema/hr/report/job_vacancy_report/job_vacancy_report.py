# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    job_vacancy = get_job_vacancy(filters)

    if not job_vacancy:
        frappe.msgprint('No records found')
        return columns, job_vacancy

    for d in job_vacancy:
        row = frappe._dict({
            'date': d.date,
            'branch': d.branch,
            'status': d.status,
            'department': d.department,
            'position': d.position,
            'qualification': d.qualification,
            'education_type': d.education_type,
            'quantity': d.quantity,
            'experience': d.experience,
            'deadline_date': d.deadline_date,
            'salary_scale_name': d.salary_scale_name,
            'level': d.level,
            'scale': d.scale,
            'basic_salary': d.basic_salary,



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
            'fieldname': 'status',
            'label': "Status",
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
            'fieldname': 'department',
            'label': "Department",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'position',
            'label': "Position",
            'fieldtype': 'data',
            'width': '120'
        },
        {
            'fieldname': 'qualification',
            'label': "Qualification",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'education_type',
            'label': "Education Type ",
            'fieldtype': 'Data',
            'width': '120'
        },
        
        {
            'fieldname': 'experience',
            'label': "Experience",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'deadline_date',
            'label': "Deadline Date",
            'fieldtype': 'date',
            'width': '120'
        },
        {
            'fieldname': 'quantity',
            'label': "Quantity",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'salary_scale_name',
            'label': "Salary Scale Name",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'level',
            'label': "Level",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'scale',
            'label': "Scale",
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'basic_salary',
            'label': "Basic Salary",
            'fieldtype': 'date',
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

    if filters.get("branch"):
        conditions += "and branch = '%s'" % filters["branch"]
    if filters.get("department"):
        conditions += "and department = '%s'" % filters["department"]
    if filters.get("position"):
        conditions += "and position = '%s'" % filters["position"]
    return conditions


def get_job_vacancy(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql(
        """select *
        from `tabJob Opening`
        where  %s"""
        % conditions,
        as_dict=1,
    )
