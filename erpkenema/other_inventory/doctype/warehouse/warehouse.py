# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Warehouse(Document):

	def before_insert(self):
		doc = frappe.db.sql(
						f""" SELECT MAX(requisition_section) as last_number FROM `tabWarehouse` """, as_dict=1)
		if not doc[0].last_number:
			self.requisition_section = 1
		else:
			self.requisition_section = doc[0].last_number + 1
