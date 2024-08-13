# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from pydoc import doc
from frappe.model.document import Document
from frappe.utils import money_in_words, flt

class CreditSalesAttachment(Document):
	
	def before_save(self):
		self.total,self.vat,self.total_inc_vat,self.total_for_vat_items=0,0,0,0
		for item in self.purchased_medicine:
	
			if item.vat: 
				self.vat += (item.unit_purchase_cost*item.vat*item.quantity)    
				self.total += (item.total_price - item.unit_purchase_cost*item.vat*item.quantity)
				self.total_for_vat_items += flt(item.total_price)
			else:
				self.total += item.total_price
			
			self.total_inc_vat = self.total + self.vat
			self.amount_in_words = money_in_words(self.total_inc_vat, main_currency = "Birr")
	
	def on_submit(self):
		for item in self.purchased_medicine:
			#subtract from sales area store
			doc = frappe.get_doc('Sales Area Store', item.item_code)
			doc.quantity = doc.quantity - item.quantity
			doc.save()
