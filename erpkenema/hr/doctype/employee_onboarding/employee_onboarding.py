# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EmployeeOnboarding(Document):
    
 def before_insert(self):
        doc = frappe.db.sql(
            f""" SELECT MAX(refno) as last_number FROM `tabEmployee Onboarding` """, as_dict=1)
        if not doc[0].last_number:
            self.refno = 1
        else:
            self.refno = doc[0].last_number + 1


@frappe.whitelist()
def get_phone(doctype, docname):
    doc = frappe.get_doc(doctype, docname)
    return doc.phone_number


@frappe.whitelist()
def get_field_data():
    dct = {}
    try:
        logged_user_email = frappe.session.user
        finance_head_doc = frappe.db.sql(
            f"""SELECT * FROM `tabFinance` WHERE status = 'Active' """, as_dict=1)
        hr_manager_doc = frappe.db.sql(
            f"""SELECT * FROM `tabHR Manager` WHERE name = '{logged_user_email}' and status = 'Active' """, as_dict=1)
        hq_manager_doc = frappe.db.sql(
            f"""SELECT * FROM `tabHead Quarter Manager` WHERE status = 'Active' """, as_dict=1)
        dct = {
            'process_by': hr_manager_doc[0].full_name,
            'process_by_email': hr_manager_doc[0].name,
            'approved_by': hq_manager_doc[0].full_name,
            'approved_by_email': hq_manager_doc[0].name,
            'finance_head': finance_head_doc[0].full_name,
            'finance_head_email': finance_head_doc[0].name

        }
    except:

        dct = {
            'process_by': '',
            'process_by_email': '',
            'approved_by': '',
            'approved_by_email': '',
            'finance_head': '',
            'finance_head_email': ''
        }
    return dct


@frappe.whitelist()
def get_qualification(job_applicant):
	qualification = frappe.db.sql(
            f""" SELECT * FROM `tabEducational Qualification` WHERE parent = '{job_applicant}'""", as_dict=True)
	return qualification
