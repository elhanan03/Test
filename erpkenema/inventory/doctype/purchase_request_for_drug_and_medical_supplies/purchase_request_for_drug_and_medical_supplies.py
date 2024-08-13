# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Purchaserequestfordrugandmedicalsupplies(Document):	
	def before_insert(self): 
		doc = frappe.db.sql(
			f""" SELECT MAX(requisition_section) as last_number FROM `tabPurchase request for drug and medical supplies` """, as_dict=1)
		if not doc[0].last_number:
			self.requisition_section = 1
		else:
			self.requisition_section = doc[0].last_number + 1



@frappe.whitelist()
def get_data():
	dct = {}
	try:
		logged_user_email = frappe.session.user

		store_manager_doc = frappe.db.sql(f"""SELECT * FROM `tabStore Manager` WHERE name = '{logged_user_email}' and status='Active' """, as_dict=1)	

		branch_manager_doc = frappe.db.sql(f"""SELECT * FROM `tabBranch Manager` WHERE branch = '{store_manager_doc[0].branch}'  and status='Active' """, as_dict=1)

		operation_manager_doc = frappe.db.sql(f"""SELECT * FROM `tabOperation Manager` WHERE status='Active' """, as_dict=1)

		dct = {
			'branch': store_manager_doc[0].branch,
			'requested_by': store_manager_doc[0].full_name,
			'approved_by': branch_manager_doc[0].full_name,
			'authorized_by': operation_manager_doc[0].full_name,
			'requested_by_email': store_manager_doc[0].name,
			'approved_by_email': branch_manager_doc[0].name,
			'authorized_by_email': operation_manager_doc[0].name
		}
	except:

		dct = {
			'branch': '',
			'requested_by': '',
			'approved_by': '',
			'authorized_by': '',
			'requested_by_email': '',
			'approved_by_email': '',
			'authorized_by_email': ''
		}

	return dct
