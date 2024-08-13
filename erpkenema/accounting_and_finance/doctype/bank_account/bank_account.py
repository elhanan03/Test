# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BankAccount(Document):
	pass


@frappe.whitelist()
def get_account_number(doctype, doc):
	doctype="`tab"+doctype+"`"
	dct = {}
	doc = frappe.db.sql(
		f""" select * from {doctype} where name='{doc}'""", as_dict=True)
	dct = {
		'bank_account_no': doc[0].bank_account_no
	}
	return dct
