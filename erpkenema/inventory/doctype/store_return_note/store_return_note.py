# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StoreReturnNote(Document):
    def before_insert(self):
        doc = frappe.db.sql(
            f""" SELECT MAX(refno) as last_number FROM `tabStore Return Note` """, as_dict=1)
        if not doc[0].last_number:
            self.refno = 1
        else:
            self.refno = doc[0].last_number + 1

    def before_save(self):
        total=0
        if self.from_doc == 'Sales Area Store':
            if self.return_type == 'Other':
                for item in self.other_items:
                    total+=item.total_cost
            else:
                for item in self.damaged_or_expired_items:
                    total+=item.total_cost
        
        if self.from_doc == 'Inventory Area Store':
            for item in self.damaged_or_expired_items_from_inventory:
                total+=item.total_cost

        self.total = total


    def on_submit(self):
        if self.from_doc == 'Sales Area Store':
           
            if self.return_type == 'Other':
                for item in self.other_items:
                    #subtract from sales area store
                    doc = frappe.get_doc('Sales Area Store', item.item_code)
                    doc.quantity = doc.quantity - item.quantity
                    doc.save()

                    # add to inventory area store
                    doc = frappe.new_doc("Inventory Area Store")
                    doc.date = self.date
                    doc.kenema_pharmacy_drug_shop_number = self.branch_number
                    doc.supplier = item.supplier
                    # doc.supplier_name = self.supplier_name
                    # doc.purchase_invoice_number = self.purchase_invoice_number
                    doc.purchase_type = item.purchase_type
                    doc.brand = item.brand
                    doc.manufacturer = item.manufacturer
                    doc.country = item.country
                    doc.item_code = item.item_code.split('-', 1)[0]
                    doc.batch_number = item.batch_number
                    doc.barcode = doc.item_code
                    doc.pharmacological_category = item.pharmacological_category
                    doc.description = item.description
                    # doc.image = item.image
                    doc.unit = item.unit
                    doc.exp_date = item.exp_date
                    doc.quantity = item.quantity
                    doc.unit_purchase_cost = item.unit_cost
                    doc.total_purchase_cost = item.total_cost
                    doc.profit = item.profit_margin
                    # doc.uspbv = item.uspbv
                    doc.uspbv = item.profit_margin * item.unit_cost + item.unit_cost
                    doc.vat = item.vat
                    doc.unit_selling_price = item.unit_selling_price
                    # doc.enter_quantity = item.enter_quantity
                    # doc.retail_price = item.retail_price
                    # doc.total_retail_pricepiece = item.total_retail_pricepiece
                    # doc.enter_qty_on_piece = item.enter_qty_on_piece
                    # doc.retail_price_strip = item.retail_price_strip
                    # doc.remark = item.remark
                    doc.insert()

            else:
                # subtract from sales area store
                for item in self.damaged_or_expired_items:
                    doc = frappe.get_doc('Sales Area Store', item.item_code)
                    doc.quantity = doc.quantity - item.quantity
                    doc.save()

                    # add to out of service item doctype
                    doc = frappe.new_doc("Out of service items")
                    doc.branch_number = self.branch_number
                    if self.return_type == 'Expired':
                        doc.type = 'Expired Item'
                        doc.exp_date = item.exp_date
                    else:
                        doc.type = 'Damaged Item'
                        doc.damaged_date = item.damaged_date

                    doc.supplier = item.supplier
                    doc.item_code = item.item_code.split('-', 1)[0]
                    doc.purchase_type = item.purchase_type
                    doc.description = item.description
                    doc.unit = item.unit
                    doc.quantity = item.quantity
                    doc.batch_number = item.batch_number
                    doc.pharmacological_category = item.pharmacological_category
                    doc.brand = item.brand
                    doc.manufacturer = item.manufacturer
                    doc.country = item.country
                    doc.unit_cost = item.unit_cost
                    doc.total_cost = item.total_cost
                    doc.insert()

        if self.from_doc == 'Inventory Area Store':
            # subtract from inventory area store
            for item in self.damaged_or_expired_items_from_inventory:
                doc = frappe.get_doc('Inventory Area Store', item.item_code)
                doc.quantity = doc.quantity - item.quantity
                doc.total_purchase_cost = doc.quantity * doc.unit_purchase_cost
                doc.save()

                # add to out of service item doctype
                doc = frappe.new_doc("Out of service items")
                doc.branch_number = self.branch_number
                if self.return_type == 'Expired':
                    doc.type = 'Expired Item'
                    doc.exp_date = item.exp_date
                else:
                    doc.type = 'Damaged Item'
                    doc.damaged_date = item.damaged_date

                doc.supplier = item.supplier
                doc.item_code = item.item_code.split('-', 1)[0]
                doc.purchase_type = item.purchase_type
                doc.description = item.description
                doc.unit = item.unit
                doc.quantity = item.quantity
                doc.batch_number = item.batch_number
                doc.pharmacological_category = item.pharmacological_category
                doc.brand = item.brand
                doc.manufacturer = item.manufacturer
                doc.country = item.country
                doc.unit_cost = item.unit_cost
                doc.total_cost = item.total_cost
                doc.insert()


@frappe.whitelist()
def get_expired_items(doctype, date, branch_number):
    doc = "`tab"+doctype+"`"
    expired_items = frappe.db.sql(
        f""" SELECT * FROM {doc} WHERE kenema_pharmacy_drug_shop_number = '{branch_number}' and exp_date <= '{date}'""", as_dict=True)
    return expired_items


@frappe.whitelist()
def get_data():
    dct = {}
    roles = frappe.get_roles(frappe.session.user)
    logged_user_email = frappe.session.user

    try:
        if "Dispensary" in roles:

            dispensary_doc = frappe.db.sql(
                f"""SELECT * FROM `tabDispensary` WHERE name = '{logged_user_email}' and status = 'Active' """, as_dict=1)

            store_manager_doc = frappe.db.sql(
                f"""SELECT * FROM `tabStore Manager` WHERE branch = '{dispensary_doc[0].branch}' and status = 'Active' """, as_dict=1)

            branch_manager_doc = frappe.db.sql(
                f"""SELECT * FROM `tabBranch Manager` WHERE branch = '{dispensary_doc[0].branch}' and status = 'Active' """, as_dict=1)

            dct = {
                'branch_number': dispensary_doc[0].branch,
                'prepared_by': dispensary_doc[0].full_name,
                'approved_by': branch_manager_doc[0].full_name,
                'received_by': store_manager_doc[0].full_name,
                'received_by_email': store_manager_doc[0].name,
                'prepared_by_email': dispensary_doc[0].name,
                'approved_by_email': branch_manager_doc[0].name
            }

        elif "Store Manager" in roles:

            store_manager_doc = frappe.db.sql(
                f"""SELECT * FROM `tabStore Manager` WHERE name = '{logged_user_email}' and status = 'Active' """, as_dict=1)

            dispensary_doc = frappe.db.sql(
                f"""SELECT * FROM `tabDispensary` WHERE branch = '{store_manager_doc[0].branch}' and status = 'Active' """, as_dict=1)

            branch_manager_doc = frappe.db.sql(
                f"""SELECT * FROM `tabBranch Manager` WHERE branch = '{store_manager_doc[0].branch}' and status = 'Active' """, as_dict=1)

            dct = {
                'branch_number': store_manager_doc[0].branch,
                'prepared_by': store_manager_doc[0].full_name,
                'approved_by': branch_manager_doc[0].full_name,
                'received_by': store_manager_doc[0].full_name,
                'received_by_email': store_manager_doc[0].name,
                'prepared_by_email': store_manager_doc[0].name,
                'approved_by_email': branch_manager_doc[0].name
            }

    except:
        dct = {
            'branch_number': '',
            'prepared_by': '',
            'approved_by': '',
            'received_by': '',
            'received_by_email': '',
            'prepared_by_email': '',
            'approved_by_email': ''
        }

    return dct
