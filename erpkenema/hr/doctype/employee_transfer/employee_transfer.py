# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EmployeeTransfer(Document):
    def on_submit(self):
        doc = frappe.get_doc("Employee", self.employee)
        doc.branch = self.to_branch
        doc.department = self.department1
        doc.designation = self.designation1
        doc.role = self.role1
        doc.save()

    def before_insert(self):
        doc = frappe.db.sql(
            f""" SELECT MAX(requisition_number) as last_number FROM `tabEmployee Transfer` """, as_dict=1)
        if not doc[0].last_number:
            self.requisition_number = 1
        else:
            self.requisition_number = doc[0].last_number + 1


@frappe.whitelist()
def get_field_data():
    dct = {}
    try:
        hr_manager_doc = frappe.db.sql(
            f"""SELECT * FROM `tabHR Manager` where status = 'Active' """, as_dict=1)

        dct = {
            'approved_by': hr_manager_doc[0].full_name,
            'approved_by_email': hr_manager_doc[0].name,

        }
    except:

        dct = {

            'approved_by': '',
            'approved_by_email': ''
        }
    return dct


@frappe.whitelist()
def get_employee_data(name):
    dct = {}
    try:
        employee = frappe.db.sql(
            f"""SELECT * FROM `tabEmployee` where status = 'Active' and name='{name}'""", as_dict=1)

        dct = {

            'from_branch': employee[0].branch,
            'department': employee[0].department,
            'designation': employee[0].designation,
            'role': employee[0].role,

        }
    except:

        dct = {

            'from_branch': '',
            'department': '',
            'designation': '',
            'role': '',
        }
    return dct
