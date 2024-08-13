# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import money_in_words


class Loanmanagement(Document):
	def before_save(self):
		self.basic_salary_in_words = money_in_words(
			self.basic_salary, main_currency="Birr")

		self.total_requested = self.basic_salary * self.requested_month
		self.monthly_payment = self.total_requested / 12


@frappe.whitelist()
def get_data():
	dct = {}
	try:

		hr_manager_doc = frappe.db.sql(
			f"""SELECT * FROM `tabHR Manager` WHERE status = 'Active' """, as_dict=1)

		dct = {
			'hr_manager': hr_manager_doc[0].full_name if hr_manager_doc else "",
			'hr_manager_email': hr_manager_doc[0].name if hr_manager_doc else ""

		}
	except:
		dct = {
			'hr_manager': '',
			'hr_manager_email': '',

		}
	return dct
