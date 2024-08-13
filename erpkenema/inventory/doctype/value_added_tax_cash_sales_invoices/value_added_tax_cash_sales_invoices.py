# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ValueAddedTaxCashSalesInvoices(Document):
	
	def before_save(self):
		self.total,self.vat,self.total_inc_vat=0,0,0
		for item in self.purchased_medicine:
	
			if item.vat: 
				self.vat += (item.unit_purchase_cost*item.vat*item.quantity)    
				self.total += (item.total_price - item.unit_purchase_cost*item.vat*item.quantity)
			else:
				self.total += item.total_price
			
			self.total_inc_vat = self.total + self.vat
			self.amount_in_words = money_in_words(self.total_inc_vat)

	def on_submit(self):
		for item in self.purchased_medicine:
			#subtract from sales area store
			doc = frappe.get_doc('Sales Area Store', item.item_code)
			doc.quantity = doc.quantity - item.quantity
			doc.save()