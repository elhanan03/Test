# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GLEntry(Document):
	def before_insert(self):
		doc = frappe.db.sql(
				f""" SELECT MAX(id_no) as last_number FROM `tabGL Entry` """, as_dict=1)
		if not doc[0].last_number:
			self.id_no = 1
		else:
			self.id_no = doc[0].last_number + 1
