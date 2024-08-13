# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EmployeeOnboardRequestForm(Document):
    def before_insert(self):
        doc = frappe.db.sql(
            f""" SELECT MAX(refno) as last_number FROM `tabEmployee Onboard Request Form` """, as_dict=1)
        if not doc[0].last_number:
            self.refno = 1
        else:
            self.refno = doc[0].last_number + 1


    def on_submit(self):
        for item in self.list_of_jobs:
            doc = frappe.new_doc("Job Opening")
            doc.branch = self.branch
            doc.employee_onboard_request = self.name
            doc.department = item.department
            doc.position = item.position
            doc.qualification = item.qualification
            doc.education_type = item.education_type
            doc.quantity = item.quantity
            doc.experience = item.experience
            # doc.deadline_date = item.deadline_date
            # doc.status = item.status
            doc.salary_scale_name = item.salary_scale_name
            doc.level = item.level
            doc.scale = item.scale
            doc.basic_salary = item.basic_salary
            # doc.job_description = item.job_description
            doc.insert()


@frappe.whitelist()
def get_data():
    dct = {}
    try:
        logged_user_email = frappe.session.user
        
        department_head_doc = frappe.db.sql(
            f"""SELECT * FROM `tabDepartment Head` WHERE name = '{logged_user_email}' and status = 'Active' """, as_dict=1)
        branch_manager_doc = frappe.db.sql(
            f"""SELECT * FROM `tabBranch Manager` WHERE name = '{logged_user_email}' and status = 'Active' """, as_dict=1)
        hr_manager_doc = frappe.db.sql(
            f"""SELECT * FROM `tabHR Manager` WHERE status = 'Active' """, as_dict=1)
        hq_manager_doc = frappe.db.sql(
            f"""SELECT * FROM `tabHead Quarter Manager` WHERE status = 'Active' """, as_dict=1)
        dct = {
            'branch': branch_manager_doc[0].branch,
            'requested_by': branch_manager_doc[0].full_name,
            'branch': department_head_doc[0].branch,
            'requested_by': department_head_doc[0].full_name,
            'requested_by_email': branch_manager_doc[0].name,
            'process_by': hr_manager_doc[0].full_name,
            'process_by_email': hr_manager_doc[0].name,
            'approved_by': hq_manager_doc[0].full_name,
            'approved_by_email': hq_manager_doc[0].name,
        }
    except:

        dct = {
            'branch': '',
            'requested_by': '',
            'requested_by_email': '',
            'process_by': '',
            'Process_by_email': '',
            'approved_by': '',
            'approved_by_email': ''
        }
    return dct


@frappe.whitelist()
def get_basic_salary(salary_scale_name, level, scale):
    doc = frappe.db.sql(
        f"""SELECT * FROM `tabSalary Structure` WHERE name1= '{salary_scale_name}' and level= '{level}' and scale='{scale}' """, as_dict=True)
    if doc:
        return doc[0].amount
    else:
        return 0
