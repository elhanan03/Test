# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StockAdjustment(Document):
	def before_insert(self):
			doc = frappe.db.sql(
				f""" SELECT MAX(refno) as last_number FROM `tabStock Adjustment` """, as_dict=1)
			if not doc[0].last_number:
				self.refno = 1
			else:
				self.refno = doc[0].last_number + 1

	def before_submit(self):
		for item in self.items_list:
			doc = frappe.get_doc("Inventory Area Store", item.item_code)
			doc.quantity = doc.quantity + item.adjusted_quantity
			doc.total_purchase_cost = doc.quantity * doc.unit_purchase_cost
			doc.save()


