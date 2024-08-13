# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PurchaseRequestforNonmedicalitems(Document):
 def before_insert(self):
        doc = frappe.db.sql(
            f""" SELECT MAX(requisition_section) as last_number FROM `tabPurchase Request for Non-medical items` """, as_dict=1)
        if not doc[0].last_number:
            self.requisition_section = 1
        else:
            self.requisition_section = doc[0].last_number + 1


@frappe.whitelist()
def get_data():
    dct = {}
    try:
        logged_user_email = frappe.session.user
        operation_manager_doc = frappe.db.sql(
            f"""SELECT * FROM `tabOperation Manager` WHERE name = '{logged_user_email}' and status = 'Active' """, as_dict=1)
        dct = {
            'requested_by': operation_manager_doc[0].full_name,
            'requested_by_email': operation_manager_doc[0].name,
        }
    except:

        dct = {
            'requested_by': '',
            'requested_by_email': ''
        }
    return dct
