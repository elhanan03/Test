# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LeaveApplication(Document):
	def before_insert(self):
            doc = frappe.db.sql(
                f""" SELECT MAX(refno) as last_number FROM `tabLeave Application` """, as_dict=1)
            if not doc[0].last_number:
                self.refno = 1
            else:
                self.refno = doc[0].last_number + 1

@frappe.whitelist()
def get_data():
	dct = {}
	try:
		logged_user_email = frappe.session.user
		branch_manager_doc = frappe.db.sql(
			f"""SELECT * FROM `tabBranch Manager` WHERE name = '{logged_user_email}' and status = 'Active' """, as_dict=1)
		hr_manager_doc = frappe.db.sql(
                    f"""SELECT * FROM `tabHR Manager` WHERE status = 'Active' """, as_dict=1)
		dct = {
			'branch_name': branch_manager_doc[0].branch if branch_manager_doc else "",
			'branch_manager_name': branch_manager_doc[0].full_name if branch_manager_doc else "",
			'branch_manager_email': branch_manager_doc[0].name if branch_manager_doc else "",
			'hr_manager': hr_manager_doc[0].full_name if hr_manager_doc else "",
			'hr_manager_email': hr_manager_doc[0].name if hr_manager_doc else "",

		}
	except:
		dct = {
			'branch_name': '',
			'branch_manager_name': '',
			'branch_manager_email': '',
			'hr_manager': '',
			'hr_manager_email': '',

		}
	return dct
