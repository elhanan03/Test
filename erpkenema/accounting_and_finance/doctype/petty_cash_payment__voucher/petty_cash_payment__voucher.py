# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import money_in_words, flt


class PettyCashPaymentVoucher(Document):
    def before_save(self):
        self.amount_in_words = money_in_words(
            self.payable_amounts_in_figure, main_currency="Birr")

        debit, credit = 0, 0
        for item in self.accounts:
            debit += flt(item.debit)

        for item in self.accounts:
            credit += flt(item.credit)

        self.total_debit = debit
        self.total_credit = credit

        if self.total_debit != self.total_credit:
            frappe.throw("Total Credit and Total Debit must be equal")

    def on_submit(self):
            if self.allocated_budget:
                doc = frappe.get_doc('Budget Allocation Page',
                                     self.allocated_budget)
                if doc.left_balance-self.payable_amounts_in_figure <= doc.amount*0.2:
                    frappe.throw("Left balance less than " +
                                 "20% " + "of allocated amount")
                doc.left_balance = doc.left_balance - self.payable_amounts_in_figure
                doc.save()

    def before_insert(self):
        doc = frappe.db.sql(
            f""" SELECT MAX(requisition_section) as last_number FROM `tabPetty Cash Payment  Voucher` """, as_dict=1)
        if not doc[0].last_number:
            self.requisition_section = 1
        else:
            self.requisition_section = doc[0].last_number + 1


@frappe.whitelist()
def get_data():
    dct = {}
    try:
        logged_user_email = frappe.session.user

        cashier_doc = frappe.db.sql(
            f"""SELECT * FROM `tabCashier` WHERE name = '{logged_user_email}' and status = 'Active'""", as_dict=1)

        if cashier_doc:
            branch_accountant_doc = frappe.db.sql(
                f"""SELECT * FROM `tabBranch Accountant` WHERE branch = '{cashier_doc[0].branch}' and status = 'Active' """, as_dict=1)

            branch_manager_doc = frappe.db.sql(
                f"""SELECT * FROM `tabBranch Manager` WHERE branch = '{cashier_doc[0].branch}' and status = 'Active' """, as_dict=1)

            dct['branch'] = cashier_doc[0].branch
            dct['prepared_by'] = cashier_doc[0].full_name
            dct['prepared_by_email'] = cashier_doc[0].name
            dct['approved_by'] = branch_accountant_doc[0].full_name
            dct['approved_by_email'] = branch_accountant_doc[0].name
            dct['authorized_by'] = branch_manager_doc[0].full_name
            dct['authorized_by_email'] = branch_manager_doc[0].name
        else:
            hq_cashier_doc = frappe.db.sql(
                f"""SELECT * FROM `tabHQ Cashier` WHERE name = '{logged_user_email}' and status = 'Active'""", as_dict=1)

            hq_accountant_doc = frappe.db.sql(
                f"""SELECT * FROM `tabHead Quarter Accountant` WHERE status = 'Active'""", as_dict=1)

            finance_doc = frappe.db.sql(
                f"""SELECT * FROM `tabFinance` WHERE status = 'Active'""", as_dict=1)

            dct['prepared_by'] = hq_cashier_doc[0].full_name
            dct['prepared_by_email'] = hq_cashier_doc[0].name

            dct['approved_by'] = hq_accountant_doc[0].full_name
            dct['approved_by_email'] = hq_accountant_doc[0].name

            dct['authorized_by'] = finance_doc[0].full_name
            dct['authorized_by_email'] = finance_doc[0].name
    except:
        dct = {
            'branch': '',
            'prepared_by': '',
            'approved_by': '',
            'authorized_by': '',
            'prepared_by_email': '',
            'approved_by_email': '',
            'authorized_by_email': '',
        }
    return dct
