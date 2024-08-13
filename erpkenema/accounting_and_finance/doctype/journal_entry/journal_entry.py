# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cint, cstr, flt, fmt_money, formatdate, get_link_to_form, nowdate

class JournalEntry(Document):
	def before_insert(self):
		doc = frappe.db.sql(
			f""" SELECT MAX(id_no) as last_number FROM `tabJournal Entry` """, as_dict=1)
		if not doc[0].last_number:
			self.id_no = 1
		else:
			self.id_no = doc[0].last_number + 1


	def on_submit(self):
		for item in self.account_entry:
				doc = frappe.new_doc("GL Entry")
				doc.posting_date = self.posting_date
				doc.party_type = item.party_type
				doc.party = item.party
				doc.account_entry = item.name
				doc.account_name = item.account_name
				doc.account_number = item.account_number
				doc.credit = item.credit
				doc.debit = item.debit
				doc.root = item.root
				doc.insert()

		debit, credit = 0, 0
		for item in self.account_entry:
				debit += flt(item.debit)

		for item in self.account_entry:
			credit += flt(item.credit)

		self.total_debit = debit
		self.total_credit = credit

		if self.total_debit != self.total_credit:
			frappe.throw("Total Credit and Total Debit must be equal")
			


# 	def validate_debit_credit_amount(self):
# 		for d in self.get("account_entry"):
# 			if not flt(d.debit) and not flt(d.credit):
# 				frappe.throw(
# 					_("Row {0}: Both Debit and Credit values cannot be zero").format(d.idx))

# 	def validate_total_debit_and_credit(self):
# 		self.set_total_debit_credit()
# 		if self.difference:
# 			frappe.throw(
# 				_("Total Debit must be equal to Total Credit. The difference is {0}").format(
# 					self.difference)
# 			)

# 	def set_total_debit_credit(self):
# 		self.total_debit, self.total_credit, self.difference = 0, 0, 0
# 		for d in self.get("account_entry"):
# 			if d.debit and d.credit:
# 				frappe.throw(
# 					_("You cannot credit and debit same account at the same time"))

# 			self.total_debit = flt(self.total_debit) + \
# 							flt(d.debit)
# 			self.total_credit = flt(self.total_credit) + \
# 							flt(d.credit)

# 		self.difference = flt(self.total_debit, self.precision("total_debit")) - flt(
# 			self.total_credit, self.precision("total_credit")
# 		)
			

# @frappe.whitelist()
# def get_balance(self):
# 	if not self.get("account_entry"):
# 			msgprint(_("'Entries' cannot be empty"), raise_exception=True)
# 	else:
# 			self.total_debit, self.total_credit = 0, 0
# 			diff = flt(self.difference, self.precision("difference"))

# 			# If any row without amount, set the diff on that row
# 			if diff:
# 				blank_row = None
# 				for d in self.get("account_entry"):
# 					if not d.credit_in_account_currency and not d.debit_in_account_currency and diff != 0:
# 						blank_row = d

# 				if not blank_row:
# 					blank_row = self.append("account_entry", {})

# 				blank_row.exchange_rate = 1
# 				if diff > 0:
# 					blank_row.credit_in_account_currency = diff
# 					blank_row.credit = diff
# 				elif diff < 0:
# 					blank_row.debit_in_account_currency = abs(diff)
# 					blank_row.debit = abs(diff)

# 			self.validate_total_debit_and_credit()
