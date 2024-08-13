# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MonthlySalaryStructure(Document):
    pass


@frappe.whitelist()
def get_previous_month(previous_month):
    previous_month = frappe.db.sql(
        f""" SELECT * FROM `tabSalary Detail` WHERE parent='{previous_month}'""", as_dict=True)
    return previous_month
