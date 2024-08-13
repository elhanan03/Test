# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class InventoryItems(Document):

	def before_insert(self): 
			doc = frappe.db.sql(
				f""" SELECT MAX(code) as last_number FROM `tabInventory Items` """, as_dict=1)
			if not doc[0].last_number:
				self.code = 1
			else:
				self.code = doc[0].last_number + 1

			self.item_code = self.code

 