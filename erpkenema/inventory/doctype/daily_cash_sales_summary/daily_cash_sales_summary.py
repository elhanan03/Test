# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import money_in_words, flt


class DailyCashsalesSummary(Document):
    def before_save(self):
        sales_ticket_amount, total_vat = 0, 0
        for item in self.sales_breakdown:
            sales_ticket_amount += flt(item.amount_in_birr)
            total_vat += flt(item.vat)

        self.sales_ticket_amount = sales_ticket_amount
        self.total_vat = total_vat

        total_cash_over, total_cash_short = 0, 0,
        for item in self.variance:
            total_cash_over += flt(item.overage_birr)
            total_cash_short += flt(item.shortage_birr)

        self.total_cash_over = total_cash_over
        self.total_cash_short = total_cash_short


@frappe.whitelist()
def get_items(sales_date, branch_number):
    items = frappe.db.sql(
        f""" SELECT cashier_full_name, GROUP_CONCAT(prepared) as dispensary_list, GROUP_CONCAT(name) as item_list, GROUP_CONCAT(total_inc_vat) as amount_list,sum(total_inc_vat) as total, sum(vat) as vat FROM `tabSales Attachment` WHERE sales_type='Cash Sales' and workflow_state="Paid" and date ='{sales_date}' and branch_number='{branch_number}' group by cashier_email""", as_dict=True)
    return items


@frappe.whitelist()
def get_data():
    try:
        logged_user_email = frappe.session.user
        branch_accountant_doc = frappe.db.sql(
            f"""SELECT * FROM `tabBranch Accountant` WHERE name = '{logged_user_email}'""", as_dict=1)
    except:
        pass

    return branch_accountant_doc[0].branch
