# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ConsignmentSalesPaymentConfirmationForm(Document):
	pass



@frappe.whitelist()
def get_consignment_items(branch_number, ref_num):

    items = frappe.db.sql(f""" SELECT * FROM `tabGood Receiving Voucher` WHERE name='{ref_num}' """, as_dict=True)
    return items