# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class CreditPurchaseRegister(Document):
    def before_save(self):
        debit_total, credit_total = 0, 0
        for data in self.credit_purchase:
            debit_total += data.debit
            credit_total += data.credit
        self.grand_debit_total = debit_total
        self.grand_credit_total = credit_total

    def before_insert(self):
        doc = frappe.db.sql(
            f""" SELECT MAX(requisition_section) as last_number FROM `tabCredit Purchase Register` """, as_dict=1)
        if not doc[0].last_number:
            self.requisition_section = 1
        else:
            self.requisition_section = doc[0].last_number + 1


@frappe.whitelist()
def get_items(branch, from_date, to_date):
    items = frappe.db.sql(
        f""" SELECT * FROM `tabGood Receiving Voucher` WHERE date >='{from_date}' and date <='{to_date}' and branch_number='{branch}' and purchase_type = 'Credit Purchase' """, as_dict=True)
    return items
