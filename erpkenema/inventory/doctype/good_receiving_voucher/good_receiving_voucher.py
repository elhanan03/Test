# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class GoodReceivingVoucher(Document):

    def before_insert(self):
        doc = frappe.db.sql(
            f""" SELECT MAX(requisition_number) as last_number FROM `tabGood Receiving Voucher` """, as_dict=1)
        if not doc[0].last_number:
            self.requisition_number = 1
        else:
            self.requisition_number = doc[0].last_number + 1

    def before_save(self):
        total_purchase_cost = 0
        total_vatable_purchase_cost = 0
        for item in self.items_received:
            total_purchase_cost += item.total_purchase_cost
            if item.vatable_item:
                total_vatable_purchase_cost += item.total_purchase_cost
        self.total = total_purchase_cost
        self.total_vatable = total_vatable_purchase_cost

    def on_submit(self):
        doc = frappe.new_doc("Credit Payment")
        doc.date = self.date
        doc.branch_number = self.branch_number
        doc.grv_no = self.name
        doc.fs_no = self.purchase_invoice_number
        doc.supplier = self.supplier_name
        doc.total = self.total
        doc.total_vatable = self.total_vatable
        doc.insert()

        for item in self.items_received:
            doc = frappe.new_doc("Inventory Area Store")
            doc.date = self.date
            doc.kenema_pharmacy_drug_shop_number = self.branch_number
            doc.supplier = self.supplier
            doc.supplier_name = self.supplier_name
            doc.purchase_invoice_number = self.purchase_invoice_number
            doc.purchase_type = self.purchase_type
            doc.consignment_number = self.consignment_number
            doc.brand = item.brand
            doc.manufacturer = item.manufacturer
            doc.country = item.country
            doc.item_code = item.item_code
            doc.batch_number = item.batch_number
            doc.barcode = item.barcode
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
            doc.enter_quantity = item.enter_quantity
            doc.retail_price = item.retail_price
            doc.total_retail_pricepiece = item.total_retail_pricepiece
            doc.enter_qty_on_piece = item.enter_qty_on_piece
            doc.retail_price_strip = item.retail_price_strip
            doc.remark = item.remark
            doc.insert()


@frappe.whitelist()
def get_mpr_items(purchase_order):
    items = frappe.db.sql(
        f""" SELECT * FROM `tabMPR_Child_Table` where parent='{purchase_order}'""", as_dict=True)
    return items


@frappe.whitelist()
def get_data():
    dct = {}
    try:
        logged_user_email = frappe.session.user
        store_manager_doc = frappe.db.sql(
            f"""SELECT * FROM `tabStore Manager` WHERE name = '{logged_user_email}' and status = 'Active' """, as_dict=1)
        branch_manager_doc = frappe.db.sql(
            f"""SELECT * FROM `tabBranch Manager` WHERE branch = '{store_manager_doc[0].branch}' and status = 'Active' """, as_dict=1)

        dct = {
            'branch_number': store_manager_doc[0].branch,
            'received_by': store_manager_doc[0].full_name,
            'posted_by': branch_manager_doc[0].full_name,
            'posted_by_email': branch_manager_doc[0].name
        }

    except:

        dct = {
            'branch_number': '',
            'received_by': '',
            'posted_by': '',
            'posted_by_email': ''
        }

    return dct
