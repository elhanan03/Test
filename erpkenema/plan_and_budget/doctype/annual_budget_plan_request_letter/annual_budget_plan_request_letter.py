# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AnnualBudgetplanRequestLetter(Document):
	def before_insert(self):
		doc = frappe.db.sql(
            f""" SELECT MAX(requisition_section) as last_number FROM `tabAnnual Budget plan Request Letter` """, as_dict=1)
		if not doc[0].last_number:
			self.requisition_section = 1
		else:
			self.requisition_section = doc[0].last_number + 1


@frappe.whitelist()
def get_data():
	dct = {}
	try:
		logged_user_email = frappe.session.user
		plan_doc = frappe.db.sql(
			f"""SELECT * FROM `tabPlan and Budget Manager` WHERE name = '{logged_user_email}' and status = 'Active' """, as_dict=1)
		
		dct = {
			'plan_and_budget_manager': plan_doc[0].full_name,
		   	'plan_and_budget_manager_email': plan_doc[0].name,
			
		}
	except:

		dct = {
			'plan_and_budget_manager': '',
		   	'plan_and_budget_manager_email': ''
			
		}
	return dct
