# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ActionPlan(Document):
    def before_insert(self):
        doc = frappe.db.sql(
                f""" SELECT MAX(requisition_section) as last_number FROM `tabAction Plan` """, as_dict=1)
        if not doc[0].last_number:
            self.requisition_section = 1
        else:
            self.requisition_section = doc[0].last_number + 1

@frappe.whitelist()
def get_data():
    dct = {}
    try:
        logged_user_email = frappe.session.user
        branch_doc = frappe.db.sql(
            f"""SELECT * FROM `tabBranch Manager` WHERE name = '{logged_user_email}' and status = 'Active'""", as_dict=1)
        plan_manager_doc = frappe.db.sql(
            f"""SELECT * FROM `tabPlan and Budget Manager` WHERE status = 'Active'""", as_dict=1)
        dct = {
            'branch': branch_doc[0].branch,
            'prepared_by': branch_doc[0].full_name,
            'approved_by': plan_manager_doc[0].full_name
        }
    except:
        dct = {
            'branch': '',
            'prepared_by': '',
            'approved_by': ''
        }
    return dct


@frappe.whitelist()
def get_previous_performance(previous_performance):
    previous_performance = frappe.db.sql(
        f""" SELECT * FROM `tabMonthly_Performance_Report_Child` WHERE parent='{previous_performance}'""", as_dict=True)
    return previous_performance
