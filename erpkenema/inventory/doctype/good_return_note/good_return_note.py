# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt
class GoodReturnNote(Document):
	
	def before_save(self):
		total_purchase_cost=0
		for item in self.items_list:
			# calculate total
			total_purchase_cost+=flt(item.total_purchase_cost)

			if self.workflow_state=='Approved' and self.return_type=='Near Expiry':
				doc = frappe.get_doc('Inventory Area Store', item.doc_name)
				doc.quantity = doc.quantity - item.quantity
				doc.total_purchase_cost = doc.quantity * doc.unit_purchase_cost
				doc.save()

			if self.workflow_state=='Approved' and self.return_type=='Consignment Out':
				doc = frappe.get_doc('Out of service items', item.doc_name)
				doc.quantity = doc.quantity - item.quantity
				doc.total_cost = doc.quantity * doc.unit_cost
				doc.save()

		self.total = total_purchase_cost


@frappe.whitelist()
def get_items(branch_number, return_type, supplier, from_date, to_date):
	if return_type=="Near Expiry":
		items = frappe.db.sql(f""" SELECT * FROM `tabInventory Area Store` WHERE kenema_pharmacy_drug_shop_number = '{branch_number}' and exp_date >='{from_date}' and exp_date <='{to_date}' and supplier_name='{supplier}' and purchase_type='Credit Purchase' """, as_dict=True)
		return items

	if return_type=="Consignment Out":
		items = frappe.db.sql(f""" SELECT * FROM `tabOut of service items` WHERE branch_number = '{branch_number}' and exp_date <='{from_date}' and supplier='{supplier}' and purchase_type='Consignment In' """, as_dict=True)
		return items


@frappe.whitelist()
def get_data():
	dct = {}
	try:
		logged_user_email = frappe.session.user
		store_manager_doc = frappe.db.sql(f"""SELECT * FROM `tabStore Manager` WHERE name = '{logged_user_email}' and status = 'Active' """, as_dict=1)	
					
		branch_manager_doc = frappe.db.sql(f"""SELECT * FROM `tabBranch Manager` WHERE branch = '{store_manager_doc[0].branch}' and status = 'Active'  """, as_dict=1)

		dct = {
			'branch': store_manager_doc[0].branch,
			'prepared_by': store_manager_doc[0].full_name,
			'approved_by': branch_manager_doc[0].full_name,
			'prepared_by_email': store_manager_doc[0].name,
			'approved_by_email': branch_manager_doc[0].name,
		}

	except:

		dct = {
			'branch': '',
			'prepared_by': '',
			'approved_by': '',
			'prepared_by_email': '',
			'approved_by_email': ''
		}

	return dct