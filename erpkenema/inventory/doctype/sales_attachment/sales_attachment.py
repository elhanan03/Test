# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

from frappe.utils import nowdate, formatdate
import frappe
from frappe.model.document import Document
from frappe.utils import money_in_words, flt

class SalesAttachment(Document):
    def before_save(self):
        self.total = self.vat = self.total_inc_vat = self.total_for_vat_items = self.total_purchase_cost = 0

        for item in self.purchased_medicine:
            if item.vat:
                self.vat += (item.unit_purchase_cost *
                             item.vat * item.quantity)
                self.total += (item.total_price -
                               item.unit_purchase_cost * item.vat * item.quantity)
                self.total_for_vat_items += flt(item.total_price)
            else:
                self.total += item.total_price

            self.total_purchase_cost += item.total_purchase_cost
            self.total_inc_vat = self.total + self.vat
            self.amount_in_words = money_in_words(
                self.total_inc_vat, main_currency="Birr")

    def on_submit(self):
        for item in self.purchased_medicine:
            # subtract from sales area store
            doc = frappe.get_doc('Sales Area Store', item.item_code)
            doc.quantity -= item.quantity
            doc.save()

    # Validate the credit limit and block the the buyer from buying an item greater then one with in a month  
    
    def validate(self):
        if self.sales_type == "Credit Sales":
            credit_limit = float(self.credit_limit or 0)
            total_cost = float(self.total_inc_vat or 0)
            customer = self.to

            # Check if any purchased medicine has a quantity of 0
            for item in self.purchased_medicine:
                if item.quantity == 0:
                    frappe.throw("It is not allowed to send an item with a quantity of 0 to a cashier.")

            # Check if the total cost exceeds the credit limit
            if credit_limit < total_cost:
                frappe.throw("Credit limit exceeded. Please review the order.")

            # Check if the customer has already made a purchase this month
            current_month = formatdate(nowdate(), "yyyy-MM")
            existing_purchase = frappe.db.sql("""
                SELECT SUM(total_inc_vat)
                FROM `tabSales Attachment`
                WHERE `to` = %s
                    AND docstatus = 1
                    AND DATE_FORMAT(date, '%%Y-%%m') = %s
            """, (customer, current_month))[0][0]

            if existing_purchase and existing_purchase > 0:
                frappe.throw("You have already made a purchase this month.")

            total_purchases = (existing_purchase or 0) + total_cost

            if total_purchases > credit_limit:
                frappe.throw("Credit limit exceeded. Please review the order.")
        elif self.sales_type == "Cash Sales":
            # Allow override for Cash Customer
            for item in self.purchased_medicine:
                if item.quantity == 0:
                    frappe.throw("It is not allowed to send an item with a quantity of 0 to a cashier.")
        else:
            frappe.throw("Invalid sales type.")



@frappe.whitelist()
def get_data():
    dct = {}
    try:
        logged_user_email = frappe.session.user
        dispenser_doc = frappe.get_doc('Dispensary', logged_user_email)
        branch_data = frappe.get_doc('Kenema Branches', dispenser_doc.branch)

        dct = {
            'branch_number': dispenser_doc.branch,
            'subcity': branch_data.subcity,
            'woreda': branch_data.woreda,
            'house_number': branch_data.house_number,
            'prepared': dispenser_doc.full_name,
            'prepared_by_email': dispenser_doc.name
        }
    except:
        dct = {
            'branch_number': '',
            'subcity': '',
            'woreda': '',
            'house_number': '',
            'prepared': '',
            'prepared_by_email': ''
        }
    return dct
