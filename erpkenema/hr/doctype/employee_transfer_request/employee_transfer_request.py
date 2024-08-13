# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeTransferRequest(Document):
	def before_insert(self):
			doc = frappe.db.sql(
				f""" SELECT MAX(requisition_number) as last_number FROM `tabEmployee Transfer Request` """, as_dict=1)
			if not doc[0].last_number:
				self.requisition_number = 1
			else:
				self.requisition_number = doc[0].last_number + 1


@frappe.whitelist()
def get_field_data():
	dct = {}
	try:
		hr_manager_doc = frappe.db.sql(
			f"""SELECT * FROM `tabHR Manager` where status = 'Active' """, as_dict=1)
		hq_manager_doc = frappe.db.sql(
			f"""SELECT * FROM `tabHead Quarter Manager` WHERE status = 'Active' """, as_dict=1)
		dct = {
			'approved_by': hr_manager_doc[0].full_name,
			'approved_by_email': hr_manager_doc[0].name,
			'authorized_by': hq_manager_doc[0].full_name,
			'authorized_by_email': hq_manager_doc[0].name,
		}
	except:

		dct = {
			# 'employee': '',
			'authorized_by': '',
			'authorized_by_email': '',
			'approved_by': '',
			'approved_by_email': ''
		}
	return dct
