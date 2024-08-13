# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StockTransferMemo(Document):
    def before_insert(self):
        doc = frappe.db.sql(
            f""" SELECT MAX(refno) as last_number FROM `tabStock Transfer Memo` """, as_dict=1)
        if not doc[0].last_number:
            self.refno = 1
        else:
            self.refno = doc[0].last_number + 1
            
    def before_save(self):
        total_purchase_cost = 0
        for item in self.stm:
            total_purchase_cost += item.total_purchase_cost
        self.total = total_purchase_cost

    def on_submit(self):
        for item in self.stm:
            # subtract from the current branch
            doc = frappe.get_doc('Inventory Area Store', item.item_code)
            doc.quantity = doc.quantity - item.quantity
            doc.total_purchase_cost = doc.quantity * doc.unit_purchase_cost
            doc.save()

            # add to the other branch
            doc = frappe.new_doc("Inventory Area Store")
            doc.purchase_type = "Transfer In"
            doc.date = self.date
            doc.kenema_pharmacy_drug_shop_number = self.to_branch
            doc.item_code = item.item_code.split('-', 1)[0]
            doc.batch_number = item.batch_number
            doc.pharmacological_category = item.pharmacological_category
            doc.description = item.description
            doc.image = item.image
            doc.unit = item.unit
            doc.exp_date = item.exp_date
            doc.quantity = item.quantity
            doc.unit_purchase_cost = item.unit_purchase_cost
            doc.total_purchase_cost = item.total_purchase_cost
            doc.profit = item.profit
            doc.uspbv = item.uspbv
            doc.vat = item.vat
            doc.unit_selling_price = item.unit_selling_price
            doc.remark = item.remarks
            doc.insert()


@frappe.whitelist()
def get_child_data(doc):
    rcd = frappe.db.sql(
        f""" SELECT * FROM `tabStoch Transfer Request Child` WHERE parent='{doc}'""", as_dict=True)
    return rcd


@frappe.whitelist()
def get_data(doc):
    rcd = frappe.db.sql(
        f""" SELECT * FROM `tabStock Transfer Requisition Form` WHERE name='{doc}'""", as_dict=True)
    return rcd


@frappe.whitelist()
def get_field_data():
    dct = {}
    try:
        logged_user_email = frappe.session.user
        store_manager_doc = frappe.db.sql(
            f"""SELECT * FROM `tabStore Manager` WHERE name = '{logged_user_email}' and status = 'Active' """, as_dict=1)
        dct = {
            'from_branch': store_manager_doc[0].branch,
            'issued_by': store_manager_doc[0].full_name,
            'issued_by_email': store_manager_doc[0].name,
        }
    except:

        dct = {
            'from_branch': '',
            'issued_by': '',
            'issued_by_email': ''
        }
    return dct


@frappe.whitelist()
def get_store_manager(to_branch):
    dct = {}
    try:
        store_manager_doc = frappe.db.sql(
            f""" SELECT * FROM `tabStore Manager` where branch='{to_branch}' and status = 'Active' """, as_dict=True)
        dct = {
            'received_by': store_manager_doc[0].full_name,
            'received_by_email': store_manager_doc[0].name
        }
    except:
        dct = {
            'received_by': '',
            'received_by_email': ''
        }
    return dct
