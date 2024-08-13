# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class OverTime(Document):
	pass


@frappe.whitelist()
def get_data():
	dct = {}
	try:
		logged_user_email = frappe.session.user
		branch_accountant_doc = frappe.db.sql(
			f"""SELECT * FROM `tabBranch Accountant` WHERE name = '{logged_user_email}' and status = 'Active' """, as_dict=1)
		branch_manager_doc = frappe.db.sql(
			f"""SELECT * FROM `tabBranch Manager` WHERE branch = '{branch_accountant_doc[0].branch}' and status = 'Active' """, as_dict=1)
		finance_doc = frappe.db.sql(
                    f"""SELECT * FROM `tabFinance` WHERE status = 'Active'""", as_dict=1)
		hr_manager_doc = frappe.db.sql(
			f"""SELECT * FROM `tabHR Manager` WHERE status = 'Active' """, as_dict=1)
		dct = {
			'branch': branch_accountant_doc[0].branch,
			'prepared_by': branch_accountant_doc[0].full_name,
		   	'prepared_by_email': branch_accountant_doc[0].name,
			'approved_by': branch_manager_doc[0].full_name,
			'approved_by_email': branch_manager_doc[0].name,
			'finance_head': finance_doc[0].full_name if finance_doc else "",
			'finance_head_email': finance_doc[0].name if finance_doc else "",
			'hr_manager': hr_manager_doc[0].full_name if hr_manager_doc else "",
			'hr_manager_email': hr_manager_doc[0].name if hr_manager_doc else "",
		}
	except:

		dct = {
			'branch': '',
			'prepared_by': '',
		   	'prepared_by_email': '',
			'approved_by': '',
			'approved_by_email': '',
			'finance_head': '',
			'finance_head_email': '',
			'hr_manager': '',
			'hr_manager_email': '',
		}
	return dct
