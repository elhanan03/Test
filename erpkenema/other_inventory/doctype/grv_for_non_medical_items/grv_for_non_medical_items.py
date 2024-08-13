# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GRVForNonMedicalItems(Document):

	def before_save(self):
		total_cost = 0
		for item in self.non_medical_items:
				total_cost += item.total_cost
		self.total = total_cost

	def on_submit(self):
		for item in self.non_medical_items:
			doc = frappe.new_doc("Warehouse")
			doc.date = self.date
			doc.supplier = self.supplier
			doc.supplier_name = self.supplier_name
			doc.purchase_order = self.purchase_order
			doc.item_name = item.item_name
			doc.item_category = item.item_category
			doc.brand = item.brand
			doc.manufacturer = item.manufacturer
			doc.uom = item.uom
			doc.quantity = item.quantity
			doc.unit_cost = item.unit_cost
			doc.total_cost = item.total_cost
			doc.remark = item.remark
			doc.insert()

	def before_insert(self):
			doc = frappe.db.sql(
				f""" SELECT MAX(requisition_section) as last_number FROM `tabGRV For Non Medical Items` """, as_dict=1)
			if not doc[0].last_number:
				self.requisition_section = 1
			else:
				self.requisition_section = doc[0].last_number + 1

@frappe.whitelist()
def get_items(purchase_order):
	items = frappe.db.sql(
            f""" SELECT * FROM `tabNon Medical Items Child` WHERE parent = '{purchase_order}'""", as_dict=True)
	return items
