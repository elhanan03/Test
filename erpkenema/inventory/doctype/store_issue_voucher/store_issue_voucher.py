# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
class StoreIssueVoucher(Document):
	
	def before_insert(self): 
		doc = frappe.db.sql(
			f""" SELECT MAX(srequisition) as last_number FROM `tabStore Issue Voucher` """, as_dict=1)
		if not doc[0].last_number:
			self.srequisition = 1
		else:
			self.srequisition = doc[0].last_number + 1

	def on_submit(self):
		for item in self.siv:
			#subtract from inventory area store
			doc = frappe.get_doc('Inventory Area Store', item.item_code)
			doc.quantity = doc.quantity - item.issued_qty
			doc.total_purchase_cost = doc.quantity * doc.unit_purchase_cost
			doc.save()


			#add to sales area store
			doc = frappe.new_doc("Sales Area Store")
			doc.date = self.date
			doc.kenema_pharmacy_drug_shop_number = self.branch_number
			doc.purchase_type = item.purchase_type
			doc.supplier = item.supplier
			doc.supplier_name = item.supplier_name
			doc.brand = item.brand
			doc.manufacturer = item.manufacturer
			doc.country = item.country
			doc.item_code = item.item_code.rsplit('-', 4)[0]
			doc.barcode = doc.item_code
			doc.batch_number = item.batch_number
			doc.pharmacological_category = item.pharmacological_category
			doc.description = item.description
			doc.unit = item.to
			doc.exp_date = item.exp_date
			doc.quantity = item.quantity_issued_to_sales
			doc.vat = item.vat
			doc.unit_selling_price = item.unit_selling_price
			doc.unit_purchase_cost = item.unit_purchase_cost
			doc.total_selling_price = item.total_selling_price_before_vat
			doc.profit_margin = item.profit_margin
			# doc.remark = item.remarks
			doc.insert()


@frappe.whitelist()
def get_data():
	dct = {}
	try:
	
		logged_user_email = frappe.session.user 
			
		dispensary_doc = frappe.db.sql(f"""SELECT * FROM `tabDispensary` WHERE name = '{logged_user_email}' and status='Active' """, as_dict=1)	

		sales_head_doc = frappe.db.sql(f"""SELECT * FROM `tabSales Head` WHERE branch = '{dispensary_doc[0].branch}' and status='Active' """, as_dict=1)

		store_manager_doc = frappe.db.sql(f"""SELECT * FROM `tabStore Manager` WHERE branch = '{dispensary_doc[0].branch}' and status='Active' """, as_dict=1)

		dct = {
			'branch_number': dispensary_doc[0].branch,
			'requested_by': dispensary_doc[0].full_name,
			'approved_by': sales_head_doc[0].full_name,
			'issued_by': store_manager_doc[0].full_name,
			'requested_by_email': dispensary_doc[0].name,
			'approved_by_email': sales_head_doc[0].name,
			'issued_by_email': store_manager_doc[0].name
		}

	except:

		dct = {
			'branch_number': '',
			'requested_by': '',
			'approved_by': '',
			'issued_by': '',
			'requested_by_email': '',
			'approved_by_email': '',
			'issued_by_email': ''
		}

	return dct