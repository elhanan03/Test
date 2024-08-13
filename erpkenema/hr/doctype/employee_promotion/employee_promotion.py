# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeePromotion(Document):
    def before_insert(self):
        doc = frappe.db.sql(
            f""" SELECT MAX(refno) as last_number FROM `tabEmployee Promotion` """, as_dict=1)
        if not doc[0].last_number:
            self.refno = 1
        else:
            self.refno = doc[0].last_number + 1
    def on_submit(self):
        doc = frappe.get_doc("Employee", self.employee)
        doc.employement_type = self.to_employement_type
        doc.department = self.to_department
        doc.designation = self.to_position
        doc.save()
