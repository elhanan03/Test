# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import money_in_words


class ValueAddedTaxCreditSalesInvoice(Document):

    def before_save(self):
        self.total, self.vat, self.total_inc_vat, self.total_for_vat_items = 0, 0, 0, 0
        for item in self.patient_list:
            self.total_for_vat_items += item.total_for_vat_items
            self.total += item.total
            self.vat += item.vat
            self.total_inc_vat += item.prescription_amount
            self.amount_in_words = money_in_words(
                self.total_inc_vat, main_currency="Birr")


@frappe.whitelist()
def get_items(from_branch, to_org, from_date, to_date):
    items = frappe.db.sql(
        f""" SELECT * FROM `tabSales Attachment` WHERE branch_number='{from_branch}' and organization='{to_org}' and date >='{from_date}' and date<='{to_date}'""", as_dict=True)
    return items
