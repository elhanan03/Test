# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import money_in_words, flt


class PaymentRequest(Document):
	def before_insert(self):
		doc = frappe.db.sql(
			f""" SELECT MAX(requisition_section) as last_number FROM `tabPayment Request` """, as_dict=1)
		if not doc[0].last_number:
			self.requisition_section = 1
		else:
			self.requisition_section = doc[0].last_number + 1

	def before_save(self):
		self.amount_in_words = money_in_words(
			self.amount_in_figure, main_currency="Birr")

	
@frappe.whitelist()
def get_value(doc, doc_type):
	d = "tab"+doc
	rcd = frappe.db.sql(
		f""" SELECT * FROM `{d}` WHERE name='{doc_type}'""", as_dict=True)
	return rcd


@frappe.whitelist()
def get_data():
	dct = {}
	try:
		logged_user_email = frappe.session.user

		finance_doc = frappe.db.sql(
			f"""SELECT * FROM `tabFinance` WHERE status = 'Active'""", as_dict=1)
		hr_manager_doc = frappe.db.sql(
			f"""SELECT * FROM `tabHR Manager` WHERE name = '{logged_user_email}' and status = 'Active' """, as_dict=1)
		deputy_manager_doc = frappe.db.sql(
			f"""SELECT * FROM `tabDeputy Manager` WHERE status = 'Active' """, as_dict=1)
		hq_manager_doc = frappe.db.sql(
			f"""SELECT * FROM `tabHead Quarter Manager` WHERE status = 'Active' """, as_dict=1)

		dct = {
			'finance_head': finance_doc[0].full_name if finance_doc else "",
			'finance_head_email': finance_doc[0].name if finance_doc else "",
			'hr_manager': hr_manager_doc[0].full_name if hr_manager_doc else "",
			'hr_manager_email': hr_manager_doc[0].name if hr_manager_doc else "",
			'deputy_manager': deputy_manager_doc[0].full_name if deputy_manager_doc else "",
			'deputy_manager_email': deputy_manager_doc[0].name if deputy_manager_doc else "",
			'hq_manager': hq_manager_doc[0].full_name if hq_manager_doc else "",
			'hq_manager_email': hq_manager_doc[0].name if hq_manager_doc else "",
		}
	except:
		dct = {
			'finance_head': '',
			'finance_head_email': '',
			'hr_manager': '',
			'hr_manager_email': '',
		   	'deputy_manager': '',
		   	'deputy_manager_email': '',
			'hq_manager': '',
		   	'hq_manager_email': ''
		}
	return dct
