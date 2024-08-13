# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BudgetRequest(Document):
	def before_insert(self):
		doc = frappe.db.sql(
				f""" SELECT MAX(requisition_section) as last_number FROM `tabBudget Request` """, as_dict=1)
		if not doc[0].last_number:
			self.requisition_section = 1
		else:
			self.requisition_section = doc[0].last_number + 1

	def before_save(self):
		total_cost = 0
		for item in self.list_of_items:
			total_cost += item.total_cost
		self.total = total_cost

@frappe.whitelist()
def get_data():
	dct = {}
	try:
		logged_user_email = frappe.session.user

		finance_doc = frappe.db.sql(
			f"""SELECT * FROM `tabFinance` WHERE name = '{logged_user_email}' and status = 'Active'""", as_dict=1)
		hr_manager_doc = frappe.db.sql(
			f"""SELECT * FROM `tabHR Manager` WHERE name = '{logged_user_email}' and status = 'Active' """, as_dict=1)
		branch_manager_doc = frappe.db.sql(
			f"""SELECT * FROM `tabBranch Manager` WHERE name = '{logged_user_email}' and status = 'Active' """, as_dict=1)
		operation_manager_doc = frappe.db.sql(
			f"""SELECT * FROM `tabOperation Manager` WHERE status = 'Active' """, as_dict=1)
		hq_manager_doc = frappe.db.sql(
			f"""SELECT * FROM `tabHead Quarter Manager` WHERE status = 'Active' """, as_dict=1)
			
		dct = {
			'branch_name': branch_manager_doc[0].branch if branch_manager_doc else "",
			'branch_manager_name': branch_manager_doc[0].full_name if branch_manager_doc else "",
			'branch_manager_email': branch_manager_doc[0].name if branch_manager_doc else "",
			'finance_head': finance_doc[0].full_name if finance_doc else "",
			'finance_head_email': finance_doc[0].name if finance_doc else "",
			'hr_manager': hr_manager_doc[0].full_name if hr_manager_doc else "",
			'hr_manager_email': hr_manager_doc[0].name if hr_manager_doc else "",
			'operation_manager': operation_manager_doc[0].full_name if operation_manager_doc else "",
			'operation_manager_email': operation_manager_doc[0].name if operation_manager_doc else "",
            'hq_manager': hq_manager_doc[0].full_name if hq_manager_doc else "",
			'hq_manager_email': hq_manager_doc[0].name if hq_manager_doc else "",
		}
	except:
		dct = {
			'branch_name': '',
			'branch_manager_name': '',
			'branch_manager_email': '',
			'finance_head': '',
			'finance_head_email': '',
			'hr_manager': '',
			'hr_manager_email': '',
		   	'operation_manager': '',
		   	'operation_manager_email': '',
			'hq_manager': '',
		   	'hq_manager_email': ''
		}
	return dct
