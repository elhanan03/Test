# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import now_datetime, add_to_date

from frappe.model.document import Document


class JobOpening(Document):
    def before_insert(self):
        doc = frappe.db.sql(
            f""" SELECT MAX(refno) as last_number FROM `tabJob Opening` """, as_dict=1)
        if not doc[0].last_number:
            self.refno = 1
        else:
            self.refno = doc[0].last_number + 1


@frappe.whitelist()
def get_basic_salary(salary_scale_name, level, scale):
    doc = frappe.db.sql(
        f"""SELECT * FROM `tabSalary Structure` WHERE name1= '{salary_scale_name}' and level= '{level}' and scale='{scale}' """, as_dict=True)
    if doc:
        return doc[0].amount
    else:
        return 0
