# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import money_in_words, flt


class ChequePaymentVoucher(Document):
	def on_submit(self):
		if self.payment_type == 'Payment For Supplier':
			for value in self.fs_number:
				
				value = str(value)
				child_name = value.split("(")[1].split(")")[0]
				# get data from Credit_Payment_Child
				doc = frappe.db.sql(f""" SELECT * FROM `tabCredit_Payment_Child` WHERE name='{child_name}' """, as_dict=True)
				# get data from Credit Payment by fs_no
				fs_number = doc[0].fs_no
				
				credit_payment_doc = frappe.get_doc('Credit Payment', fs_number)
				credit_payment_doc.status = 'Paid'
				credit_payment_doc.save()


	def before_save(self):
		self.amount_in_words = money_in_words(
			self.payable_total, main_currency="Birr")

		debit, credit = 0, 0
		for item in self.accounting_entries:
			debit += flt(item.debit)

		for item in self.accounting_entries:
			credit += flt(item.credit)

		self.total_debit = debit
		self.total_credit = credit

		if self.total_debit != self.total_credit:
			frappe.throw("Total Credit and Total Debit must be equal")

@frappe.whitelist()
def get_credit_payment_data(payee, from_date, to_date):
	
	items = frappe.db.sql(
		f""" SELECT * FROM `tabCredit Payment` WHERE date >='{from_date}' and date<='{to_date}' and supplier='{payee}' """, as_dict=True)
	
	return items


@frappe.whitelist()
def get_data():
	dct = {}
	try:
		logged_user_email = frappe.session.user

		finance_doc = frappe.db.sql(
			f"""SELECT * FROM `tabFinance` WHERE status = 'Active'""", as_dict=1)
		auditor_doc = frappe.db.sql(
                    f"""SELECT * FROM `tabAuditor` WHERE status = 'Active'""", as_dict=1)
		hq_accountant_doc = frappe.db.sql(
			f"""SELECT * FROM `tabHeadquarter Accountant` WHERE status = 'Active'""", as_dict=1)
		hr_manager_doc = frappe.db.sql(
			f"""SELECT * FROM `tabHR Manager` WHERE status = 'Active' """, as_dict=1)
		deputy_manager_doc = frappe.db.sql(
			f"""SELECT * FROM `tabDeputy Manager` WHERE status = 'Active' """, as_dict=1)
		hq_manager_doc = frappe.db.sql(
			f"""SELECT * FROM `tabHead Quarter Manager` WHERE status = 'Active' """, as_dict=1)

		dct = {
			'finance_head': finance_doc[0].full_name if finance_doc else "",
			'finance_head_email': finance_doc[0].name if finance_doc else "",
			'finance_head1': finance_doc[0].full_name if finance_doc else "",
			'finance_head_email1': finance_doc[0].name if finance_doc else "",
			'hq_accountant': hq_accountant_doc[0].full_name if hq_accountant_doc else "",
			'hq_accountant_email': hq_accountant_doc[0].name if hq_accountant_doc else "",
			'hr_manager': hr_manager_doc[0].full_name if hr_manager_doc else "",
			'hr_manager_email': hr_manager_doc[0].name if hr_manager_doc else "",
			'deputy_manager': deputy_manager_doc[0].full_name if deputy_manager_doc else "",
			'deputy_manager_email': deputy_manager_doc[0].name if deputy_manager_doc else "",
			'hq_manager': hq_manager_doc[0].full_name if hq_manager_doc else "",
			'hq_manager_email': hq_manager_doc[0].name if hq_manager_doc else "",
			'audited_by_name': auditor_doc[0].full_name if auditor_doc else "",
			'audited_by_email': auditor_doc[0].name if auditor_doc else "",
		}
	except:
		dct = {
			'finance_head': '',
			'finance_head_email': '',
			'finance_head1': '',
			'finance_head_email1': '',
			'hr_manager': '',
			'hr_manager_email': '',
		   	'deputy_manager': '',
		   	'deputy_manager_email': '',
			'hq_manager': '',
		   	'hq_manager_email': '',
			'hq_accountant': '',
		   	'hq_accountant_email': '',
			'audited_by_name': '',
		   	'audited_by_email': ''

		}
	return dct