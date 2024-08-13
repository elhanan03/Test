# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import money_in_words


class CashReceiptVoucher(Document):
    def before_save(self):
        self.amount_in_words = money_in_words(
            self.amount_in_figure, main_currency="Birr")

    def before_insert(self):
        doc = frappe.db.sql(
                f""" SELECT MAX(requisition_section) as last_number FROM `tabCash Receipt Voucher` """, as_dict=1)
        if not doc[0].last_number:
                self.requisition_section = 1
        else:
                self.requisition_section = doc[0].last_number + 1


@frappe.whitelist()
def get_data(payer, from_date, to_date):
    doc = frappe.db.sql(
        f""" SELECT SUM(total_inc_vat) as total FROM `tabSales Attachment` WHERE date>='{from_date}' and date<='{to_date}' and sales_type='Credit Sales' and organization='{payer}'""", as_dict=True)
    return doc[0].total
