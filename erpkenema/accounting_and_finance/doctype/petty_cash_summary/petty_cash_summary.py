# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PettyCashSummary(Document):
	def before_insert(self):
		doc = frappe.db.sql(
			f""" SELECT MAX(requisition_section) as last_number FROM `tabPetty Cash Summary` """, as_dict=1)
		if not doc[0].last_number:
			self.requisition_section = 1
		else:
			self.requisition_section = doc[0].last_number + 1


@frappe.whitelist()
def get_data():
	dct = {}
	try:
		logged_user_email = frappe.session.user
		branch_accountant_doc = frappe.db.sql(
			f"""SELECT * FROM `tabBranch Accountant` WHERE name = '{logged_user_email}' and status = 'Active' """, as_dict=1)
		branch_manager_doc = frappe.db.sql(
			f"""SELECT * FROM `tabBranch Manager` WHERE branch = '{branch_accountant_doc[0].branch}' and status = 'Active' """, as_dict=1)
		dct = {
			'branch': branch_accountant_doc[0].branch,
			'prepared_by': branch_accountant_doc[0].full_name,
		   	'prepared_by_email': branch_accountant_doc[0].name,
			'approved_by':branch_manager_doc[0].full_name,
			'approved_by_email': branch_manager_doc[0].name
		}
	except:

		dct = {
			'branch': '',
			'prepared_by': '',
		   	'prepared_by_email': '',
			'approved_by':'',
			'approved_by_email': ''
		}
	return dct


@frappe.whitelist()
def get_items(from_date, to_date, branch):
    items = frappe.db.sql(
        f""" SELECT payee, payable_amounts_in_figure FROM `tabPetty Cash Payment  Voucher` WHERE date >='{from_date}' and date<='{to_date}' and branch = '{branch}'""", as_dict=True)
    return items
